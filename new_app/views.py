from typing import Any
from django.http import HttpResponseBadRequest, JsonResponse
from django.db.models import Count, OuterRef, Subquery, Q, Avg,F
from django.views import View
from .models import School, Student, Course, Enrolment


class SchoolStatsView(View):
    def get(self, request, *args, **kwargs):
        # Annotate each school with the count of students enrolled in courses
        schools_with_student_count = School.objects.annotate(
            student_count=Count("students")
        )

        # Subquery to get the count of courses for each school
        subquery = (
            Course.objects.filter(school=OuterRef("pk"))
            .values("school")
            .annotate(course_count=Count("pk"))
            .values("course_count")
        )

        # Annotate each school with the count of courses
        schools_with_course_count = schools_with_student_count.annotate(
            course_count=Subquery(subquery)
        )

        # Convert queryset to a list of dictionaries for JsonResponse
        schools_data = [
            {
                "id": school.id,
                "name": school.name,
                "location": school.location,
                "student_count": school.student_count,
                "course_count": school.course_count,
            }
            for school in schools_with_course_count
        ]

        return JsonResponse({"schools": schools_data})


class EnrolledCoursesView(View):
    def get(self, request, *args, **kwargs):
        # Subquery to get a list of course IDs in which a student is enrolled
        subquery = (
            Enrolment.objects.filter(student=OuterRef("pk"))
            .values("course")
            .annotate(enrolment_count=Count("pk"))
            .values("course")
        )
        breakpoint()
        # Query to get students and courses they are enrolled in
        students_with_enrolled_courses = Student.objects.annotate(
            enrolled_course_ids=Subquery(subquery)
        ).prefetch_related("enrolments__course")
        print("students_with_enrolled_courses", students_with_enrolled_courses)
        # Convert queryset to a list of dictionaries for JsonResponse
        result_data = [
            {
                "student_id": student.id,
                "student_name": student.name,
                "enrolled_courses": list(
                    student.enrolments.values_list("course__title", flat=True)
                ),
            }
            for student in students_with_enrolled_courses
        ]

        return JsonResponse({"enrolled_courses": result_data})


class testView(View):
    def get(self, request):
        students = Student.objects.all()

        # Convert QuerySet to a list of dictionaries
        student_data = []
        for student in students:
            student_data.append(
                {
                    "id": student.id,
                    "name": student.name,
                    "fees": student.fees,
                    "cls": student.cls,
                    "school": student.school.name,
                }
            )

        return JsonResponse({"student": student_data})


# class DetailsView(View):
#     def get(self, request, *args, **kwargs):
# subquery = (
#     Enrolment.objects.filter(student=OuterRef("pk"))
#     .values("course")
# )
# students_with_enrolled_courses = Student.objects.annotate(
#     enrolled_course_ids=Subquery(subquery)
# ).prefetch_related("enrolments__course")
# print("students_with_enrolled_courses",students_with_enrolled_courses)
# # Convert queryset to a list of dictionaries for JsonResponse
# result_data = [
#     {
#         "student_id": student.id,
#         "student_name": student.name,
#         "school":student.school.name,
#         "enrolled_courses": list(
#             student.enrolments.values_list("course__title", flat=True)
#         ),
#     }
#     for student in students_with_enrolled_courses
# ]

# return JsonResponse({"enrolled_courses": result_data})


class DetailsView(View):
    def get_details_class(self, request):
        enrollments = Enrolment.objects.all()

        # Create a dictionary to store courses for each student
        student_courses_dict = {}

        for enrollment in enrollments:
            student_name = enrollment.student.name
            course_name = enrollment.course.title

            # Check if the student is already in the dictionary
            if student_name not in student_courses_dict:
                student_courses_dict[student_name] = []

            # Add the course to the list of courses for the student
            student_courses_dict[student_name].append(course_name)

        # Convert the dictionary to the desired JSON format
        enrollment_list = [{"student name": student, "enroll courses": courses} for student, courses in student_courses_dict.items()]

        # return JsonResponse({"enrollment": enrollment_list})
        return enrollment_list
    
    

    # def get(self,request):
    #     enrollments=Enrolment.objects.filter(Q(student__name='khem') | Q(student__name='raj')).filter(course__strength__gte=30)
    #     student_list_dict={}

    #     for enrollment in enrollments:
    #         student_name=enrollment.student.name
    #         course_name=enrollment.course.title

    #         if student_name not in student_list_dict:
    #             student_list_dict[student_name]=[]
    #         student_list_dict[student_name].append(course_name)
    #     student_list=[{"student name":student,"course_name":courses} for student, courses in student_list_dict.items()]

    #     return JsonResponse ({"student details":student_list})

    def get(self, request, school_id):
        students = Student.objects.filter(school__id=school_id)

        if not students:
            return JsonResponse(
                {"message": "No students found for the given school ID."}, status=404
            )

        school_name = students[
            0
        ].school.name  # Assuming all students belong to the same school

        student_list = [
            {
                "student_name": student.name,
                "student_id": student.id,
                # Add other student information as needed
            }
            for student in students
        ]

        return JsonResponse({"school_name": school_name, "students": student_list})

    # def get(self, request, *args, **kwargs):
    #     courses = Course.objects.all()
    #     print(courses)
    #     student_list = []
    #     for course in courses:
    #         for student in course.students.all():
    #             student_list.append({
    #                 'course id': course.crs_id,
    #                 'school name': course.school.name,
    #                 'student name': student.name
    #             })
    #             print(student)
    #     print(student_list)
    #     return JsonResponse({'students': student_list}, safe=False)

    # def get(self, request, *args, **kwargs):
    #     students = Student.objects.all()
    #     student_list = [{'first_name': student.name, "school name":student.school.name} for student in students]
    #     return JsonResponse({'students': student_list}, safe=False)

    # def get(self,request):
    #     enrollments=Enrolment.objects.filter(Q(student__name='khem') | Q(student__name='raj'))
    #     student_course_dict={}

    #     for enrollment in enrollments:
    #         student_name=enrollment.student.name
    #         course_name=enrollment.course.title

    #         if student_name not in student_course_dict:
    #             student_course_dict[student_name]=[]
    #         student_course_dict[student_name].append(course_name)

    #     enrollment_list=[{"student name":student, "course":course} for student,course in student_course_dict.items()]

    #     return JsonResponse({"enrollment list":enrollment_list})


# class StudentdetailsView(View):

#     def get(self, request):
#         students = self.get_student_data()
#         course=self.get_pretech_related()
#         response={"students": students,"prefecth related data":course}
#         return JsonResponse(response)

#     def get_student_data(self, request):
#         students = Student.objects.select_related('school').all()

#         student_list = [
#             {
#                 "student_name": student.name,
#                 "student_id": student.id,
#                 "school_name": student.school.name if student.school else None,
#                 # Add other student information as needed
#             }
#             for student in students
#         ]

#         return student_list
#     def get_pretech_related(self):
#         students = Student.objects.prefetch_related('courses').all()

#         student_list_pre = [
#             {
#                 "student_name": student.name,
#                 "student_id": student.id,
#                 "courses": [{"course_name": course.title, "course_id": course.id} for course in student.courses.all()],
#                 # Add other student information as needed
#             }
#             for student in students
#         ]

#         return student_list_pre


class StudentdetailsView(DetailsView):
    def get(self, request):
        students_data = self.get_student_data()
        pretech_related_data = self.get_pretech_related()
        detail_class=self.get_details_class(request)
        response_data = {
            "students": students_data,
            "prefetch_related_data": pretech_related_data,
            "details view class":detail_class,
        }
        return JsonResponse(response_data)

    def get_student_data(self):
        students = Student.objects.select_related("school").all()

        student_list = [
            {
                "student_name": student.name,
                "student_id": student.id,
                "school_name": student.school.name if student.school else None,
                # Add other student information as needed
            }
            for student in students
        ]

        return student_list
    
    def get_pretech_related(self):
        # Calculate the average fees for all students
        avg_all_students_fees = Student.objects.aggregate(avg_fees=Avg('fees'))
        print(avg_all_students_fees)

        # Fetch students with prefetch_related and filter based on individual fees
        students = (
            Student.objects.prefetch_related("courses")
            .annotate(avg_all_students_fees=Avg('fees'))
            .filter(fees__gt=F('avg_all_students_fees'))
        )

        student_list = [
            {
                "student name": student.name,
                "fees": student.fees,
                "courses": [
                    {
                        "course name": course.title,
                        "strength": course.strength,
                        "school course": course.school.name,
                    }
                    for course in student.courses.all()
                ] if student.courses.exists()
                else [],
            }
            for student in students
        ]

        return {"student details": student_list, "avg fees for all students": avg_all_students_fees}
    # def get_pretech_related(self):
    #     students = (
    #         Student.objects.prefetch_related("courses")
    #         .annotate(avg_fees=Avg("fees"))
    #         .filter(avg_fees__gte=50000)
    #     )
    #     average_fees_list = [student.avg_fees for student in students]
    #     print(average_fees_list)
    #     student_list = [
    #         {
    #             "student name": student.name,
    #             "fees": student.avg_fees,
    #             "courses": [
    #                 {
    #                     "course name": course.title,
    #                     "strength": course.strength,
    #                     "school course": course.school.name,
    #                 }
    #                 for course in student.courses.all()
    #             ]if student.courses.exists()
    #             else [],
            
    #         }
    #         for student in students
    #     ]

    #     return {"student details":student_list,"avg fees":average_fees_list}


    # def get_pretech_related(self):
    #     students = Student.objects.prefetch_related('courses').all()

    #     student_list = [
    #         {
    #             "student_name": student.name,
    #             "student_id": student.id,
    #             "courses": [{"course_name": course.title, "course_id": course.crs_id} for course in student.courses.all()],
    #             # Add other student information as needed
    #         }
    #         for student in students
    #     ]

    #     return student_list

    # def get_pretech_related(self):
    #     students = (
    #         Student.objects.prefetch_related("courses")
    #         .annotate(avg_fees=Avg("fees"))
    #         .filter(avg_fees__gte=50000)
    #     )

    #     student_list = [
    #         {
    #             "student_name": student.name,
    #             "student_fees": student.avg_fees,
    #             "student_school": student.school.name,
    #             "courses": [
    #                 {"course_name": course.title, "strength": course.strength}
    #                 for course in student.courses.all()
    #             ]
    #             if student.courses.exists()
    #             else [],
    #         }
    #         for student in students
    #     ]

    #     return student_list






# import requests
# import json
# import time

# class LiveStockDataView(View):
#     def get(self, request, symbol):
#         # NSE API URL for real-time stock data
#         api_url = "https://www.nseindia.com/api/quote-data?symbol=" + symbol

#         # Add headers to the request
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
#             'Referer': 'https://www.nseindia.com/',
#         }

#         # Send GET request to fetch stock data
#         response = requests.get(api_url, headers=headers)

#         # Check if request was successful
#         if response.status_code == 200:
#             # Parse JSON response into a Python dictionary
#             data = response.json()

#             # Extract relevant stock data
#             current_price = data['data'][0]['lastPrice']
#             day_high = data['data'][0]['dayHigh']
#             day_low = data['data'][0]['dayLow']
#             volume = data['data'][0]['totalTradedVolume']
#             change_percent = data['data'][0]['changePercent']

#             # Prepare stock data
#             stock_data = {
#                 "symbol": symbol,
#                 "current_price": current_price,
#                 "day_high": day_high,
#                 "day_low": day_low,
#                 "volume": volume,
#                 "change_percent": change_percent,
#             }

#             return JsonResponse(stock_data)
#         else:
#             # Error handling for unsuccessful requests
#             error_message = f"Error fetching stock data for symbol {symbol}"
#             if response.status_code == 404:
#                 error_message += " (symbol may be invalid)"
#             return JsonResponse({"error": error_message, "status_code": response.status_code})


# from django.http import JsonResponse
# from django.views import View
# from .nse import NseIndia

# class LiveStockDataView(View):
#     def get(self, request, symbol):
#         nse = NseIndia()

#         try:
#             TCap, FCap, LPrice, Macro, Sector, Industry, BIndustry = nse.get_stock_info(symbol)
#             stock_data = {
#                 "symbol": symbol,
#                 "total_cap": TCap,
#                 "free_float_cap": FCap,
#                 "last_price": LPrice,
#                 "macro": Macro,
#                 "sector": Sector,
#                 "industry": Industry,
#                 "basic_industry": BIndustry,
#             }
#             return JsonResponse(stock_data)
#         except Exception as e:
#             return JsonResponse({"error": f"Error fetching stock data for symbol {symbol}: {e}"}, status=500)



import pandas as pd
from django.http import JsonResponse
from django.views import View
from .nse import NseIndia

class LiveStockDataView(View):
    def get(self, request, symbol):
        nse = NseIndia()

        try:
            TCap, FCap, LPrice, Macro, Sector, Industry, BIndustry = nse.get_stock_info(symbol)
            stock_data = {
                "symbol": symbol,
                "total_cap": TCap,
                "free_float_cap": FCap,
                "last_price": LPrice,
                "macro": Macro,
                "sector": Sector,
                "industry": Industry,
                "basic_industry": BIndustry,
            }

            # Create a DataFrame from the stock data
            df = pd.DataFrame([stock_data])

            # Save to Excel file
            df.to_excel('stock_data.xlsx', index=False)

            return JsonResponse(stock_data)
        except Exception as e:
            return JsonResponse({"error": f"Error fetching and saving stock data for symbol {symbol}: {e}"}, status=500)

class ExtractStockDataView(View):
    def get(self, request):
        try:
            # Read data from Excel file into a DataFrame
            df = pd.read_excel('stock_data.xlsx')

            # Convert DataFrame to JSON
            data_json = df.to_json(orient='records')

            return JsonResponse({"data": data_json})
        except Exception as e:
            return JsonResponse({"error": f"Error extracting stock data: {e}"}, status=500)