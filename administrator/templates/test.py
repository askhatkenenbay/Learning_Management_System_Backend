import pdfkit 
pdfkit.from_url('http://127.0.0.1:8000/administrator/semester-courses', 'courses.pdf')