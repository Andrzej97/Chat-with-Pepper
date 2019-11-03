#!/usr/bin/env bash

export PYTHONPATH="$PWD"
trap "exit" SIGINT

response_from_console_enabled=false
rest_controller_port=$(python src/common_utils/parameter_provider.py "REST_API_PORT" 2>&1)
robot_socket_port=$(python src/common_utils/parameter_provider.py "ROBOT_SOCKET_PORT" 2>&1)

initialize_database(){
   python src/common_utils/database_preparing/set_init_configure.py &
}

start_rest_service(){
   echo "Initializing REST service..."
   python src/connectivity/rest/rest_controller.py &
   echo "REST service initilized successfuly!"
}

start_bot(){
  if [ $response_from_console_enabled == true ]
  then
    python src/connectivity/socket/socket_conn_bot.py -c
  else
    python src/connectivity/socket/socket_conn_bot.py
  fi
}

help(){
    echo "
      --------------------------------------------------
                Welcome in Chat-with-Pepper
      --------------------------------------------------
      You can run this script with following options:

        [-c | --console]                   enables providing responses to user questions from command line
        [-db | --initialize_database]      initilizes database with required data
        [-r | --rest]                      starts REST service
        [-b | --bot]                       starts bot
     "
}

exit(){
  echo "
  Closing Chat-with-Pepper..."
  kill -9 $(lsof -t -i tcp:$robot_socket_port,$rest_controller_port)
}


if [ "$1" == "" ]
then
  help
fi

while [ "$1" != "" ]; do
    case $1 in
        -c | --console )
            response_from_console_enabled=true
            ;;
        -db | --initialize_database )
            initialize_database
            ;;
        -h | --help )
            help
            ;;
        -r | --rest )
            start_rest_service
            ;;
        -b | --bot )
          start_bot
          ;;
    esac
    shift
done

wait