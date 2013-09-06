from flask import Blueprint
from flask import render_template, request, redirect
#from cloudmesh.provisioner.cm_launcher import cm_launcher
from cloudmesh.util.util import cond_decorator
from flask.ext.login import login_required
from cloudmesh.config.cm_config import cm_config_launcher
from cloudmesh.launcher.queue.tasks import task_launch
import cloudmesh

launch_module = Blueprint('launch  _module', __name__)

#
# ROUTE: launch  
#

# fake list of recipies which we need to get from cm_launcher
launcher_config = cm_config_launcher()
launch_recipies = launcher_config.get("recipies")
columns = launcher_config.get("columns")

@launch_module.route('/cm/launch/<host>/<recipie>')
@cond_decorator(cloudmesh.with_login, login_required)
def launch_run ():
    print "implement"
    pass

@launch_module.route('/cm/launch/launch_servers', methods = ["POST"])
@cond_decorator(cloudmesh.with_login, login_required)
def launch_servers():
    name = request.form.get("name")
    resources = request.form.getlist("resource")
    return_dict = {}
    return_dict["name"] = name
    return_dict["host_list"] = request.form.get("hostlist")
    recipies_list = []
    for r in resources:
        recipies_list.append((r,request.form.get(r+"-select")))
    return_dict["recipies"] = recipies_list
    print "+++++++++++++++++++++++++++++++++" + str(return_dict)
    task_launch.delay(return_dict)
    return "tasks have been submitted to the queue."
   
#     return_string = "in server " + server + "<br>" #+ str(resources)
#     for r in resources:
#         return_string += " start " + str(r) +" - " + str(request.form.get(r+"-select")) +"</br>"
#     return return_string


@launch_module.route('/cm/launch')
@cond_decorator(cloudmesh.with_login, login_required)
def display_launch_table():
    
    # fake list of recipies which we need to get from cm_launcher
       
    return render_template('mesh_launch.html',
                           recipies=launch_recipies,
                           columns=columns,
                           )

