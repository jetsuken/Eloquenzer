print("NOTE: Please make sure that Composer is currently installed.")
kontinue = input('Press 1 to continue, or any other to exit and check it again.')
if kontinue != 1 and kontinue != "1":
	exit()
else:
	import os, errno
	import sys
	if "win" in sys.platform:
		slash = "\\"
	else:
		slash = "/"
	scriptpath = os.path.realpath(__file__).replace(os.path.realpath(__file__).split(slash)[len(os.path.realpath(__file__).split(slash) )-1], "")
	os.chdir(scriptpath)
	try:
		import pymysql.cursors
	except:
		print("Can't import PyMySQL. Trying to install it...")
		if "win" in sys.platform:
			command = "python -m pip install --user PyMySQL"
		else:
			command = "pip install PyMySQL || pip3 install PyMySQL"
		os.system(command)
		try:
			import pymysql.cursors
		except:
			print("Eloquenzer can't install PyMySQL, please try to install manually (more info: https://github.com/PyMySQL/PyMySQL)")
			print("It's not possible continue without database connection and will stop now.")
			exit()
		print("...")
	import json

	class DBControl:
		config = {
			'host': '',
			'user': '',
			'password': '',
			'db': '',
			'charset':'utf8',
			'cursorclass':pymysql.cursors.DictCursor
		}

		def testCnx(self):
			print("Trying to connect to database...")
			try:
				connection = pymysql.connect(**self.config)
			except:
				print("...Error! Eloquenzer can't continue without DB connection and will stop now.")
				exit()
			return True
		
		def getData(self, sql):
			result = None
			connection = pymysql.connect(**self.config)
			try:
				with connection.cursor() as cursor:
					cursor.execute(sql)
					result = cursor.fetchall()
			except ValueError:
				print('Error: '+ValueError)
				result = None
			finally:
				connection.close()
			return result
		
		def regData(self, sql):
			reg = False
			affected_rows = 0;
			connection = pymysql.connect(**self.config)
			try:
				with connection.cursor() as cursor:
					affected_rows += cursor.execute(sql)
				connection.commit()
				if affected_rows > 0:
					reg = True
			except ValueError:
				print('Error: '+ValueError)
			finally:
				connection.close()
			return reg
	#=======================================================

	def make_project_dirs(dirpath):
		# dirpath = 
		print("Making dir '"+str(dirpath)+"'...")
		try:
			os.makedirs(dirpath)
			print("...Done!")
		except OSError as e:
			if e.errno != errno.EEXIST:
				print_r("...Fail! Process can't continue without '"+str(dirpath)+"' dir and will stop now. ")
				#raise
				exit()

	def make_composerJson_file(project_name, eloquent_version):
		if project_name == "" or project_name == " " or project_name == "	":
			project_name = "Generic-Project-Without-Name"
		else:
			project_name = str(project_name).replace(" ", "-")
		yson = {
			"name": str(project_name)+"/eloquent",
			"description": "Created automatically with Eloquenzer Script (by Jesus De La Torre)",
			"type": "project",
			"require": {
				"illuminate/database": eloquent_version
			},
			"autoload": {
				"psr-4": {
					"Controllers\\": "app/controllers/",
					"Models\\": "app/models/"
				}
			}
		}
		try:
			print("Trying to export composer.json file...")
			with open(scriptpath+'composer.json', 'w') as outfile:  
				json.dump(yson, outfile)
			print("...Done!")
		except:
			print("...Fail! Cannot create composer.json file. Eloquenzer can't continue without it and will stop now.")
			exit()

	def install_composer_things():
		try:
			os.chdir(scriptpath)
			print("Trying to install Composer required extensions...")
			os.system("composer install")
			os.system("composer dump-autoload -o")
			print("...Done!")
		except:
			print("...Fail! Cannot execute shell commands and Eloquenzer can't continue. Eloquenzer will stop now")
			exit()

	def create_start_file():
		txt = """
<?php
require 'config.php';
require 'vendor/autoload.php';
use Models\Database;
//Initialize Illuminate Database Connection
new Database();
?>
		"""
		try:
			print("Trying to create the start.php file...")
			with open(scriptpath+'start.php', 'w') as outfile:
				outfile.write(txt)
			print("...Done!")
		except:
			# print("Unexpected error:", sys.exc_info()[0])
			print("...Fail! Cannot create the start.php file. Eloquenzer will stop now")
			exit()

	def create_capsule():
		txt = """
<?php
 
namespace Models; 
use Illuminate\Database\Capsule\Manager as Capsule;
 
class Database {
 
	function __construct() {
		$capsule = new Capsule;
		$capsule->addConnection([
		 'driver' => DBDRIVER,
		 'host' => DBHOST,
		 'database' => DBNAME,
		 'username' => DBUSER,
		 'password' => DBPASS,
		 'charset' => 'utf8',
		 'collation' => 'utf8_unicode_ci',
		 'prefix' => '',
		]);
		// Setup the Eloquent ORM… 
		$capsule->bootEloquent();
	}
 
}
		"""
		try:
			print("Trying to create the app/models/database.php file...")
			with open(scriptpath+'app'+slash+'models'+slash+'database.php', 'w') as outfile:
				outfile.write(txt)
			print("...Done!")
		except:
			# print("Unexpected error:", sys.exc_info()[0])
			print("...Fail! Cannot create the app/models/database.php file. Eloquenzer will stop now")
			exit()

	def create_config_file(dbhost, dbname, dbusrname, dbpassword):
		txt = """<?php\n
defined("DBDRIVER")or define('DBDRIVER','mysql');
defined("DBHOST")or define('DBHOST','"""+dbhost+"""');
defined("DBNAME")or define('DBNAME','"""+dbname+"""');
defined("DBUSER")or define('DBUSER','"""+dbusrname+"""');
defined("DBPASS")or define('DBPASS','"""+dbpassword+"""');
		"""
		try:
			print("Trying to create the config.php file...")
			with open(scriptpath+'config.php', 'w') as outfile:
				outfile.write(txt)
			print("...Done!")
		except:
			print("...Fail! Cannot create the config.php file. Eloquenzer will stop now")
			exit()

	def get_model_name(table_name):
		new_name = table_name
		model_name = ""
		if str(table_name[-1:]) == 's':
			new_name = str(table_name[:-1])
		new_name_parts = new_name.split('_')
		for part in new_name_parts:
			model_name += part.capitalize()
		return model_name

	# def get_model_filename(table_name):
	# 	new_name = table_name
	# 	model_name = ""
	# 	if str(table_name[-1:]) == 's':
	# 		new_name = str(table_name[:-1])
	# 	new_name_parts = new_name.split('_')
	# 	for part in new_name_parts:
	# 		model_name += part.capitalize()
	# 	return model_name

	def get_database_schema(dbctrl):
		tables_list = dbctrl.getData("SHOW TABLES")
		tables = []
		for objeto in tables_list:
			key = "Tables_in_"+str(dbctrl.config['db'])
			# print(key)
			table_name = objeto[key]
			
			# new_name = table_name
			# model_name = ""
			# if str(table_name[-1:]) == 's':
			# 	new_name = str(table_name[:-1])
			# new_name_parts = new_name.split('_')
			# for part in new_name_parts:
			# 	model_name += part.capitalize()
			model_name = get_model_name(table_name)
			# fields = dbctrl.getData("SHOW FIELDS FROM "+str(table_name))
			hasmanies = dbctrl.getData("""
			SELECT 
				*
			FROM
			  INFORMATION_SCHEMA.KEY_COLUMN_USAGE
			WHERE
			  REFERENCED_TABLE_SCHEMA = '"""+str(dbctrl.config['db'])+"""' AND
			  REFERENCED_TABLE_NAME = '"""+str(table_name)+"""'
			""")
			table = {
				"name": table_name,
				"model_name": model_name,
				"fields": dbctrl.getData("SHOW FIELDS FROM "+str(table_name)),
				"hasmanies": hasmanies
			}
			# table['fields'] = fields
			tables.append(table)
		return tables

	def create_models(db_schema):
		for table in db_schema:
			name = table['name']
			model_name = table['model_name']
			fields = table['fields']
			hasmanies = table['hasmanies']
			txt = """
<?php
 
namespace Models;
 
use \Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\SoftDeletes;
class """+model_name+""" extends Model {
use SoftDeletes; 
	protected $table = '"""+name+"""';

	protected $fillable = [
			"""
			i = 0
			for field in fields:
				if i > 0:
					field_name = "'"+field['Field']+"',"
					txt += field_name
				i = i+1
			txt += """
	];
			"""
			for hasmany in hasmanies:
				hasmany_owned_tablename = hasmany['TABLE_NAME']
				hasmany_owned_modelname = get_model_name(hasmany_owned_tablename)
				txt += """
	public function """+hasmany_owned_tablename+"""(){
		"""+str("return $this->hasMany('Models\$modelname');").replace("$modelname", hasmany_owned_modelname)+"""
	}
				"""
			txt += """
	 
}
 
?>
			"""
			try:
				print("Trying to create the '"+model_name+"' model...")
				with open(scriptpath+'app'+slash+'models'+slash+model_name+'.php', 'w') as outfile:
					outfile.write(txt)
				print("...Done!")
			except:
				print("...Fail! Cannot create the '"+model_name+"'' model. Eloquenzer will stop now")
				exit()


	# def generate_models():
	# 	dbctrl = DBControl()
	# 	tables = 
	# 	return None

	#=======================================================
	print("=============================================================")
	print("	________										   ")
	print("   / ____/ /___  ____ ___  _____  ____  ____ ___  _____")
	print("  / __/ / / __ \/ __ `/ / / / _ \/ __ \/_  // _ \/ ___/")
	print(" / /___/ / /_/ / /_/ / /_/ /  __/ / / / / //  __/ /	")
	print("/_____/_/\____/\__, /\__,_/\___/_/ /_/ /___|___/_/	 ")
	print("   _____		 /__	   __						  ")
	print("  / ___/__________(_)___  / /_						 ")
	print("  \__ \/ ___/ ___/ / __ \/ __/						 ")
	print(" ___/ / /__/ /  / / /_/ / /_						   ")
	print("/____/\___/_/  /_/ .___/\__/						   ")
	print("				/_/									")
	print("")
	print("   BY JESUS DE LA TORRE")
	print("=============================================================")

	dbctrl = DBControl()

	eloquent_version = "5.7.1"

	project_name = input("Project Name:")
	dbhost = input("DB Host:")
	dbname = input("DB Name:")
	dbusrname = input("DB User:")
	dbpassword = input("DB Password:")
	
	make_composerJson_file(project_name, eloquent_version)

	dbctrl.config = {
		'host': dbhost,
		'user': dbusrname,
		'password': dbpassword,
		'db': dbname,
		'charset':'utf8',
		'cursorclass':pymysql.cursors.DictCursor
	}
	dbctrl.testCnx()

	make_project_dirs(scriptpath+"app")
	make_project_dirs(scriptpath+"app"+slash+"controllers")
	make_project_dirs(scriptpath+"app"+slash+"models")

	install_composer_things()

	create_config_file(dbhost, dbname, dbusrname, dbpassword)
	create_capsule()
	create_start_file()

	db_schema = get_database_schema(dbctrl)
	create_models(db_schema)


