#!/usr/bin/env python3

import aws_cdk as cdk

from new_project.new_project_stack import NewProjectStack


app = cdk.App()
NewProjectStack(app, "new-project")



app.synth()
