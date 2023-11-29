from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
import ezdxf

class FileAnalysis(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255, unique=True)
    date = models.DateField(auto_now=True)
    note = models.TextField()
    uploadfile = models.FileField(upload_to='uploads/')
    cad_value = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.filename}"

    def save(self, *args, **kwargs):
        # Set the user to the current logged-in user if available
        if not self.user_id and hasattr(self, 'request_user'):
            self.user = self.request_user

        # Set the filename based on the uploaded file
        if self.uploadfile:
            original_filename = self.uploadfile.name
            self.filename = f"{self.user.username}_{slugify(original_filename)}"

            # Calculate and set CAD value using a hypothetical CAD file parsing library
            self.cad_value = self.get_cad_value()

        super().save(*args, **kwargs)

    def get_cad_value(self):
        if not self.uploadfile:
            return 0.0

        try:
            # Create an in-memory copy of the file
            file_copy = self.uploadfile.read()

            # Parse the CAD file from the in-memory copy
            doc = ezdxf.read(file_copy)
            cad_value = self.calculate_cad_value(doc)
            return cad_value
        except Exception as e:
            # Handle parsing errors
            print(f"Error parsing AutoCAD file: {e}")
            return 0.0

    def calculate_cad_value(self, doc):
        cad_value = 0.0

        # Iterate through all entities in the drawing
        for entity in doc.modelspace().query('*'):
            if entity.dxftype() == 'LINE':
                # For simplicity, calculate the length of each line and add it to the total
                start_point = entity.dxf.start
                end_point = entity.dxf.end
                length = ((end_point[0] - start_point[0])**2 + (end_point[1] - start_point[1])**2)**0.5
                cad_value += length

        return cad_value


