from locust import HttpLocust, TaskSet, task
import string,random

def id_generator(size=6, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

class WebsiteTasks(TaskSet):
    question_no = 1
    next_btn = True
    first_question = 1
    last_question_no = 31
    def on_start(self):
        self.login()

    def login(self):
        r = self.client.get('/register/')
        r = self.client.post('/register/', 
        {'username': id_generator(), 'password1': 'password',
        'Login' : 'login', 'phone' : 'PHON',
        'college_name' : 'sd',       
        'csrfmiddlewaretoken': r.cookies['csrftoken']})
        self.csrf = r.cookies['csrftoken']

    def next_question(self):
        url = str('/'+str(self.question_no)+'/disp/')
        data = {
        'answer' : 'asd',
        'min' : '23',
        'sec' : '10',
        'nav' : 'Next',
        'status': 'yellow',
        'csrfmiddlewaretoken': self.csrf,
        }
        self.client.post(url,data)
    
    def previous_question(self):
        url = str('/'+str(self.question_no)+'/disp/')
        data = {
        'answer' : 'asd',
        'min' : '23',
        'sec' : '10',
        'nav' : 'Previous',
        'status': 'green',  
        'csrfmiddlewaretoken': self.csrf,
        }
        self.client.post(url,data)


    @task(2)
    def navigation(self):
        if self.next_btn == True and self.question_no ==  self.last_question_no:
            self.next_btn = False
        if self.next_btn == False and self.question_no == self.first_question:
            self.next_btn = True
        if self.next_btn:
            self.next_question()
            self.question_no += 1 
        else:
            self.previous_question()
            self.question_no -= 1
        
    @task(1)
    def timer(self):
        self.client.post("/timer",
            {'min':'25' , 'sec' : '10',
            'csrfmiddlewaretoken': self.csrf })

            
        
class WebsiteUser(HttpLocust):
    task_set = WebsiteTasks
    min_wait = 2*1000
    max_wait = 4000