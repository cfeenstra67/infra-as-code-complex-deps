
gen-ssh-key:
	ssh-keygen -f iac-test-key

fmt:
	black cdk/{app.py,cdk} pulumi/*.py statey/*.py
