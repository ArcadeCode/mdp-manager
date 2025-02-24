.PHONY: clean

clean:
	powershell -Command "Get-ChildItem -Path .\src, .\tests -Directory -Recurse -Filter '__pycache__' | Remove-Item -Recurse -Force"
