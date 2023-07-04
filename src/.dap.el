(dap-register-debug-template "statsbomb-api"
			     (list :type "python"
				   :request "launch"
				   :target-module "src/statsbomb-api.py"
				   :args ""
				   :cwd (expand-file-name "~/projects/soccer/statsbomb-api")
				   :env '(
					  ("PYTHONPATH" . ".")
					  )
				   :name "statsbomb-api"
				   )
			     )
(dap-register-debug-template "test-statsbomb-api"
			     (list :type "python"
				   :request "launch"
				   :target-module "unittest"
				   :args "-m"
				   :cwd (expand-file-name "~/projects/soccer/statsbomb-api")
				   :env '(
					  ("PYTHONPATH" . ".")
					  )
				   :name "statsbomb-api"
				   )
			     )
