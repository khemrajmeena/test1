from django.db import models

class School(models.Model):
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    strenth=models.IntegerField()
    
    def __str__(self):
        return self.name

class Student(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    fees = models.IntegerField()
    cls = models.IntegerField()
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students')
    
    def __str__(self):
        return self.name

class Course(models.Model):
    crs_id = models.IntegerField(primary_key=True)
    students = models.ManyToManyField(Student, through='Enrolment', related_name='courses')
    title = models.CharField(max_length=50)
    strength = models.IntegerField()
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='courses')
    
    def __str__(self):
        return self.title

class Enrolment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrolments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrolments')