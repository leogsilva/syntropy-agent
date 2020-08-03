job "noia-agent" {

  type = "system"

  constraint {
     attribute = "${attr.kernel.name}"
     value     = "linux"
   }

  group "agent" {
    count = 1
    restart {
      attempts = 20
      interval = "30m"
      delay = "15s"
      mode = "fail"
    }

    task "noia-agent" {
      driver = "raw_exec"
      resources {
        memory = 900
        cpu    = 2000
      }
    config {
      command = "/usr/local/bin/noia-agent"
      args    = ["run"]
        }
    env {
      NOIA_API_KEY='z99CuiZnMhe2qtz4LLX43Gbho5Zu9G8oAoWRY68WdMTVB9GzuMY2HNn667A752EA'
      NOIA_CONTROLLER_URL='app-controller-platform-agents.noia.network'

    }
      }

    }
  }