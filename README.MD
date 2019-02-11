<b>2016 Fortune-Telling e-commerce project based on Django using Mezzanine and Stripe.</b>

This website was originally a freelance project for a Feng Shui master, who pulled a disappearing act.
After that, I continued the project as a learning exercise and it is currently 99% functional for all the below capacities.

As such it can be considered a reference for anybody brave enough to look at messy experimental code for a Django site deployed on AWS.

This code has not been refactored or touched in a long time, Django has progressed a lot since then, and there are security updates that must be applied from current versions of packages. UPDATE BEFORE TRYING TO RUN.

Do not use the versions listed in requirements.txt

<b>Key highlights:</b>

Fortune-telling Four Pillars of Destiny algorithm. See: https://en.wikipedia.org/wiki/Four_Pillars_of_Destiny

Ecommerce shop

3 tier membership system

Payments with Stripe, including AliPay

Basic page builder

Discussion forum w/ Machine (incomplete)

Celery task scheduling

Tri-lingual with English, Simplified, and Traditional Chinese.


<b>Originally hosted on AWS Stack using:</b>

Elastic Beanstalk

Postresql

Amazon SNS messaging service

S3 for static image hosting

And

Send In Blue for emails
