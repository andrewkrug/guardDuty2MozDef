# amazon-guardduty-to-slack
Demonstrates sending Amazon GuardDuty findings to MozDef

## Prerequisites:
You must have your own instance of MozDef from Mozilla

https://github.com/mozilla/mozdef

## Step 1:
Use the CloudFormation service to execute the gd2md.template in this repository
- Add the minimum severity - example HIGH would only send high severity findings, LOW sends all findings
- Acknowledge that the template will create IAM resources and execute it

## Thats it!  The template will run for about 5 minutes and you are ready to go.
To test the template be sure that you have GuardDuty enabled in the same region.
You can then generate some sample findings.  In a few minutes, you should see
the findings showing up in the SQS created by the template.

## Developing
Full test coverage has been provided.  From the root of the project simply:

1. Create a python3 virtual env.
2. Source that and `pip3 install -r requirements.txt`
3. Run `nosetest --with-watch tests/`
4. Dev until content.

## License
This application is distributed under the
[Mozilla Public License](https://www.mozilla.org/en-US/MPL/2.0/).
