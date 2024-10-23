# JobSearch
The aim of the project is to create a job rudimentary portal site that can be 
used to search for jobs for a particular role and allows applicants to apply 
as well as un-submit their previous application. The application was 
developed using flask web framework and mongo DB for the backend. The 
front end was created using HTML and bootstrap. For the purpose of this 
project two databases were used, the first one is used to store details about 
the job roles available and the second database is used to store applicant 
information. Each job role can take upto 5 applicants and once the number 
of applicants reaches the upper limit the site will not accept anymore 
applications for that role. If a particular applicant wants to remove their 
application then the slot is freed and the slot count for that particular role 
they had applied will be increase by one. At each stage proper form 
validation is done to avoid insertion of empty data. All CRUD operations 
were performed in this project.
Create : insertion of new applicants
Read: finding whether the job role is available or not
Update: updating the value of the job role once applied or removed
Delete: removing applicant data when unsubmitted

