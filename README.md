A Django-based system that integrates GitHub and Slack to provide real-time pull request notifications (PR creation, merge, comments). It includes daily PR summaries and leverages Celery for asynchronous task processing. Ideal for developers looking to automate GitHub notifications with webhooks.


to run the project 

just clone the repo 
go to the project directory
make sure you are in the folder where compose.yml file is present 
run docker-compose up --build

the received notification would be like this 
<img width="1649" alt="Screenshot 2025-04-20 at 12 38 59 PM" src="https://github.com/user-attachments/assets/05fdce56-4669-4268-977a-7fe3be551add" />
