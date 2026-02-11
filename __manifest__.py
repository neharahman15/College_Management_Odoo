{

    'name': 'College',
    'version': '1.0',
    'summary': 'College Management',
    'license': 'LGPL-3',
    'depends': ['base', 'product','mail','account'],
    'data': ['security/ir.model.access.csv',
             'data/course_product_data.xml',
             'data/sequence_data.xml',
             'data/teacher_data.xml',
             'data/admission_data.xml',
             'data/student_email_template.xml',
             'data/teacher_email_template.xml',
             'views/college_students_views.xml',
             'views/college_teachers_views.xml',
             'views/product_template_views.xml',
             'views/college_courseproducts_views.xml',
             'views/college_student_admission_views.xml',],

    'installable': True,
    'application': True,
}