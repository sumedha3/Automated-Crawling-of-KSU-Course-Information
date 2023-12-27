from Application.models import User

def course_list(user_id):
    classes = list( User.objects.aggregate(*[
                {
                    '$lookup': {
                        'from': 'enrollment', 
                        'localField': 'user_id', 
                        'foreignField': 'user_id', 
                        'as': 'enrollments' 
                    }
                }, { 
                    '$unwind': {
                        'path': '$enrollments', 
                        'includeArrayIndex': 'enrollment_id', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$lookup': {
                        'from': 'course_info', 
                        'localField': 'enrollments.course_id', 
                        'foreignField': 'course_id', 
                        'as': 'course_info'
                    }
                }, {
                    '$unwind': {
                        'path': '$course_info',
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$match': {
                        'user_id': user_id
                    }
                }, {
                    '$sort': {
                        'course_id': 1
                    }
                }
            ]))
    return classes
