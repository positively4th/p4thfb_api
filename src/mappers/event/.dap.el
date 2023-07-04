(dap-register-debug-template "possessionmapper"
  (list :type "python"
        :args ""
        :cwd (expand-file-name "~/projects/soccer/statsbomb-api/")
        :env '(("PYTHONPATH" . "./src"))
        :target-module "src/mappers/event/possessionmapper.py"
        :request "launch"
        :name "possessionmapper"))
