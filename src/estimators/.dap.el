(dap-register-debug-template "average"
  (list :type "python"
        :args ""
        :cwd (expand-file-name "~/projects/soccer/statsbomb-api/src")
        :env '(("PYTHONPATH" . "."))
        :target-module "estimators/average.py"
        :request "launch"
        :name "average"))
