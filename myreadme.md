
open database with TablePlus
COLORS https://www.color-hex.com/color-names.html
UQ225704540DE

THIS IS THE GIT TRACKED PROJECT
rest go to archive

#deployments via heroku should be automatic
github site



1. 
# Before each project
python3 -m venv venv/myenv 
source venv/myenv/bin/activate
pip3 install -r requirements.txt
(myenv) √ m1cro6 % python3 app.py
export IAMTOKEN=$(yc iam create-token)
export FOLDERID='b1g7mdqlta9umrhfcnbv'

2
check IAMTOKEN
echo $IAMTOKEN
t1.9euelZqUk5qJx5Gaj82Kx47OyM6Qm-3rnpWaycqbnsuKmo-Ky8vJm8edy4_l8_cxHTVh-e9nHyFX_N3z93FLMmH572cfIVf8zef1656Vmo6Lzo2UjsaSmpabkJaam8vN7_0.dgVtSSfZxiB0ivM1YO3bKW6pHTLRUuJQtGIRxmg7_vkBrnEEVkQlOxyAUtDxkGCkSWkvZpFX-U7FQHcq3npYDQ

See if works if expired...DO ANYWA
export IAMTOKEN=$(yc iam create-token)
(myenv) √ m1cro6 % echo $IAMTOKEN                        
t1.9euelZqUk5qJx5Gaj82Kx47OyM6Qm-3rnpWaycqbnsuKmo-Ky8vJm8edy4_l9PdiXzBh-e9rUTqT3fT3Ig4uYfnva1E6k83n9euelZqOi86NlI7GkpqWm5CWmpvLze_9.Htw8ZE6ZVRxACGkDd_ElVT1BWAYOrt98hEVPcusfLSh5Gk9zJyOe0KXdogXDpSzUA1_bj87ZShjpkfZEwHo9AA

echo $FOLDERID 
if blank
export FOLDERID='b1g7mdqlta9umrhfcnbv'

3
Pull new code
git pull origin new

or 
git fetch origin new

may need to stash
git stash
OR
git reset --hard HEAD
 
PUSH to remote branch
git push origin new




TIMES DATES
* add setting for Translator (best as part of config) - timeZone or automatic adjustment to timezone or CET - No keep CET
* Add a minutes left in Translator email 


Deployment Heroku DONE

Github CLI
credential.helper=osxkeychain
filter.lfs.clean=git-lfs clean -- %f
filter.lfs.smudge=git-lfs smudge -- %f
filter.lfs.process=git-lfs filter-process
filter.lfs.required=true
user.name=sdplatt
user.email=87469321+sdplatt@users.noreply.github.com
git config user.email




MS7
* Add cancel button to setPrice popup!
* Word limit is 350. You used 385 words validation persists across session in CHrome
* New emails
Client is supposed to get email when job submitted with link to Job page to accept.
Client had a Reject button - now it is gone so need rejectCriteria settings.
Translator needs an email to be alerted when Client accepts Translation.
* Localize Strings!
* On Home Page 
* On Home Page Hide I am a translator button 
* On Home page remove All Users

Localization
msg.html will be ENGLISH GERMAN RUSSIAN scroll down for


Post Localization
ME
* All Services Deadline label explain this is the BEST deadline you can do
* 

Stage2
2.1 Worker
Client gets email after 6 hours if translation was submitted and he did not Accept(rate)
Job is automatically accepted

wait for chat to get better end


the Price in getPrice is the total price in EURS
also compute word price for filters


OPT 

Sort by status

During string localization allow for interpolation with current_time
my_field.choices = [('val1', f'Option 1 - {my_variable}'), ('val2', 'Option 2')]
ALT my_field.choices = [('val1', 'Option 1 - {}'.format(my_variable)), ('val2', 'Option 2')]
    deadline = RadioField("Deadline",choices=[(1,f'30 minutes'),(2,"60 minutes"),(3,"90 minutes"),(4,"120 minutes")],validators=[DataRequired()])

    
jinja2.exceptions.UndefinedError: 'None' has no attribute 'text'


MS8
Candidates inclient.views
# 1 get all clients with this to and from in service
# 2 get all clients with this to and from in service with client.deadline <= translator.deadline
# 3 add 10 minute time penalty for translator.isHuman true translator.isNative false. default true
# 4 also submit to bots identified by email? but different procedure

Annoying JINGA2 session exceptions
  File "/Users/derzessionar/prog/web/m1cro6/venv/myenv/lib/python3.11/site-packages/flask/templating.py", line 147, in render_template
    return _render(app, template, context)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/derzessionar/prog/web/m1cro6/venv/myenv/lib/python3.11/site-packages/flask/templating.py", line 130, in _render
    rv = template.render(context)
         ^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/derzessionar/prog/web/m1cro6/venv/myenv/lib/python3.11/site-packages/jinja2/environment.py", line 1301, in render
    self.environment.handle_exception()
  File "/Users/derzessionar/prog/web/m1cro6/venv/myenv/lib/python3.11/site-packages/jinja2/environment.py", line 936, in handle_exception
    raise rewrite_traceback_stack(source=source)
  File "/Users/derzessionar/prog/web/m1cro6/myProject/templates/client.html", line 1, in top-level template code
    {% extends "base.html" %}
  File "/Users/derzessionar/prog/web/m1cro6/myProject/templates/base.html", line 23, in top-level template code
    {% block content %}
  File "/Users/derzessionar/prog/web/m1cro6/myProject/templates/client.html", line 368, in block 'content'
    <li>Text: {{translation.text[:150]}}...</li>
jinja2.exceptions.UndefinedError: 'None' has no attribute 'text'

MS7
* On Home Page Hide I am a translator button
* On Home page remove All Users
* What should happen when Translation request submitted? Some sort of acknowledgement -> sending a mail to client when translator a translator accepts the request-> $10
* "Word limit is 350. You used XX words" validation persists across session in Chrome - should not persist thru pages (screenshot) -> will fix it and other error also
* "Word limit is 350. You used XX words" validation persists across session in Chrome - should not persist
* Adding number of words and average price in make request form -> $10
*Client receives notification that Translation was submitted by Translator -> $10
*Translator receives notification that Client reviewed his Translation -> $10
Add cancel button to setPrice popup. to return to first prepolated form -> $20


B0t Integration
Add Field menu Legal Technical Medical 
Change list to humanCandidates
Add list botCandidates filter based on review/from to pair
Set minimum fee to the price per word of the bot for that language combination
At the moment the jobs are sent to a list of emails all these are isHuman true.
If client sets a price below Minimum or there are no Candidates isHuman true or the algorithm suggests there will be no offers,
the work is sent to the best ranked bot

Call API 
API returns text which is submitted automatically for the chosen highest ranking engine

 
25JAN

https://www.usegolang.com/

Clean up UI
use this version in git copy code over
deplpy

Add multilingual labels for now since only 3

Add walkthru video
Make process clear to first time user.
select language select first time user


MS8 preStage2
Payment!
YandexBot

prepayment - 
quick
later allows for escrow
return to merchant to complete payment process
hardest part

cheap payment 0.03 per word will use Bot -> can be used to encourage people to use it

small texts testTranslate or microTranskate

Can then be duplicated to instaTranslate with larger texts cheap price only bots and delivered to email

This is basically Stage2

the queries are simple for the filters

COmplexity is acting as an arb for disputes must come later and be as automated
ONLY email support 
support@l1vetranslate.com
Admin dashboard

What is essentiak?
Prepayment 
YandexBot = all pairs done, can offer cheap translations
=> Can extend to non m1cro and all pairs 1nstaTranslate => users sign up
Also client always gets a result if he pays low. 
Auto-cancel function after deadline - what happens to payment?


Later Allow for multiple bots to compete against each other if equal first to return
Allow for time penalties for low ratings + 10 mins delay -> staggered email delivery when Client submits

App needs income to grow

Add spam guard
Sicherheitsabfrage: ✲
8 + 1 = 
9

Bitte lösen Sie die Rechenaufgabe richtig.

