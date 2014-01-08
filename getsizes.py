import sys, os, sqlite3
def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if os.path.exists(fp):
               total_size += os.path.getsize(fp)
    return total_size

def sizeof_fmt(num):
    for x in ['B ','KB','MB','GB']:
        if num < 1024.0 and num > -1024.0:
            return "%5.1f %s" % (num, x)
        num /= 1024.0
    return "%5.1f %s" % (num, 'TB')

def print_dir_sizes():
   #Create a temp database in memory
   connection = sqlite3.connect(":memory:")
   cursor = connection.cursor()

   cursor.execute('CREATE TABLE size_table ( \
   Directory text, \
   Size real, \
   Note text) \
   ')
   connection.commit()


   cwd = os.getcwd()

   #Start printing the progress indicator
   sys.stdout.write('Progress indicator')

   #Calculate all directory sizes, then enter them in sqlite db
   dirlist = filter(os.path.isdir, os.listdir(cwd))
   dirlist = [ d for d in os.listdir(cwd) if os.path.isdir(d) ]

   for directory in dirlist:
      folder = cwd+'/'+directory
      x_file = str(directory)
      x_size = get_size(folder)
      x_note = "DIRECTORY"
      t = (x_file, x_size, x_note)
      sql = """INSERT INTO size_table VALUES """+str(t)
      cursor.execute(sql)
      connection.commit()
      sys.stdout.write('.')
      sys.stdout.flush()

   #Calculate all file sizes, then enter them in sqlite db
   filelist = filter(os.path.isfile, os.listdir(cwd))
   filelist = [ f for f in os.listdir(cwd) if os.path.isfile(f) ]

   for file in filelist:
      folder = cwd+'/'+file
      x_file = str(file)
      x_size = os.path.getsize(file)
      x_note = "     FILE"
      t = (x_file, x_size, x_note)
      sql = """INSERT INTO size_table VALUES """+str(t)
      cursor.execute(sql)
      connection.commit()
      sys.stdout.write('.')
      sys.stdout.flush()
   print('')

   
   #Print out list of directories and sizes (sorted desc by size)
   cursor.execute("SELECT * FROM size_table ORDER BY Size DESC")
   row = cursor.fetchone()

   totalsize = 0
   while row:
       print('(' + row[2] + ') ' + sizeof_fmt(row[1]) + ' -- ' + row[0] )
       totalsize += row[1]
       row = cursor.fetchone()
   print('')
   print('TOTAL: '+ sizeof_fmt(totalsize) )

print_dir_sizes()


