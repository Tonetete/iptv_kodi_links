import sys, os, re, tkinter.filedialog, optparse

# ===== METHODS ======

class IPTV_KODI_LINKS(object):

    sections = ['--ES: VOD SERIES', '--ES: VOD DOCUMENTALES', '--ES: VOD CINE', '--ES: VOD ANIME' \
        , '--ES: VOD CLASICAS', '--ES: VOD MUSICAL', '--ES: VOD INFANTIL', '--ES: VOD ADULTOS']

    series = ['--ES: VOD SERIES', '--ES: VOD DOCUMENTALES', '--ES: VOD INFANTIL', '--ES: VOD ANIME']

    type = ['SER-', 'BRR-', 'ANI-', 'XXX-', 'INF-', 'CLA-', 'DOC-', 'MUS-']

    def __init__(self, directory, option, filename):
        self.directory = directory
        self.option = option
        self.filename = filename
        self.createFiles()

    def createFiles(self):
        f = open(self.filename, encoding="utf8")
        lines = f.readlines()
        for index, line in enumerate(lines):
            pattern_group_title = re.findall('group-title="(.*?)"', line)
            if len(pattern_group_title) > 0 and pattern_group_title[0] in self.sections:
                pattern_tvg_name = re.findall('tvg-name="(.*?)"', line)
                if len(pattern_tvg_name) == 1:
                    if self.option != 'all' and pattern_group_title[0] in self.series:
                        pattern_name = re.findall(self.option.upper(), pattern_tvg_name[0].upper())
                        if len(pattern_name) == 1:
                            name_file = re.findall('-(.*-?)', pattern_tvg_name[0])
                            if self.saveSeasonEpisodes(name_file[0], pattern_group_title[0], lines[index+1]) is None:
                                pattern_group_title[0] = self.removeSpecialCharFolderName(pattern_group_title[0])
                                self.createDirectory(self.directory + '/' + pattern_group_title[0])
                                self.saveFile(self.directory + '/' + pattern_group_title[0] + '/' + name_file[0], lines[index+1])
                    elif self.option == 'all':

                        # Not a series type, so we don't care to save in a folder series and assign patterns
                        name_file = re.findall('-(.*-?)', pattern_tvg_name[0])
                        if pattern_group_title[0] not in self.series:
                            pattern_group_title[0] = self.removeSpecialCharFolderName(pattern_group_title[0])
                            self.createDirectory(self.directory + '/' + pattern_group_title[0])
                            self.saveFile(self.directory + '/' + pattern_group_title[0] + '/' + name_file[0], lines[index + 1])
                        else:
                            if self.saveSeasonEpisodes(name_file[0], pattern_group_title[0], lines[index + 1]) is None:
                                pattern_group_title[0] = self.removeSpecialCharFolderName(pattern_group_title[0])
                                self.createDirectory(self.directory + '/' + pattern_group_title[0])
                                self.saveFile(self.directory + '/' + pattern_group_title[0] + '/' + name_file[0],
                                              lines[index + 1])

    def removeSpecialCharFolderName(self, name):
        pattern_path = re.compile('([^\s\w]|_)+')
        return pattern_path.sub('', name)

    def saveFile(self, name, url):
        file = open(name + '.strm', 'w+')
        file.write(url)
        file.close()

    def saveSeasonEpisodes(self, name, section, url):
        name = name.replace('Temporada ', 'S0')
        name = name.replace(' Ep. ', 'E')
        # pattern form of 'SE01-EP01', 'S01E01', 'se01ep01' and's01e01'
        pattern = re.search('(SE|se|S|s){1}(\d{1,2})-?(EP|ep|E|e){1}(\d{1,2})', name)
        if pattern == None:
            # pattern form of '01x01'
            pattern = re.search('(\d{1,4})x{1}(\d{1,4})', name)

        if pattern:
            pattern_season_ep = pattern.group(0)
            name = self.getName(name, pattern_season_ep)
            section = self.removeSpecialCharFolderName(section)
            self.createDirectory(self.directory + '/' + section + '/' + name)
            self.saveFile(self.directory + '/' + section + '/' + name + '/' + pattern_season_ep, url)
            return True

        else:
            return None

    def getName(self, name, pattern_season_ep):
        name = name.split(pattern_season_ep)
        pattern_name = re.compile('([^\s\w]|_)+')
        stripped_name = pattern_name.sub('', name[0])
        stripped_name = stripped_name.lstrip()
        stripped_name = stripped_name.rstrip()
        return self.unCamel(stripped_name)

    def createDirectory(self, path):
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                print('cannot create directory in ' + path)


    def unCamel(self, x):
        from functools import reduce
        return reduce(lambda a, b: a + ((b.upper() == b and (len(a) and a[-1].upper() != a[-1])) and (' ' + b) or b), x, '')

# ===== ADD OPT PARSER ======

''' Option 'all' -> obtain all media files
    Option <name> -> obtain just media files according to param name
'''

option = None

parser = optparse.OptionParser()
parser.add_option("--file",
                  action="store", dest="file_option",
                  help="flag para asignar el archivo de nuestra lista m3u")

parser.add_option("--name",
                  action="store", dest="name_option",
                  help="flag para obtener los archivos .strm del nombre de la serie o película")
parser.add_option("--all",
                  action="store_true", dest="all_option", default=False,
                  help="flag para obtener todos los archivos .strm de todas las series y películas")

(options_parser, args) = parser.parse_args()


# ===== CHECKING PARAMS ======

if options_parser.file_option is None:
    parser.print_help()
    sys.exit()

elif (options_parser.all_option == True and options_parser.name_option is not None) or (options_parser.all_option == False and options_parser.name_option is None):
    parser.print_help()
    sys.exit()

elif options_parser.all_option == True:
    option = 'all'

elif options_parser.name_option is not None:
    option = options_parser.name_option

# ===== DIRECTORY PARAMS ======

options_dir = {}
options_dir['initialdir'] = 'C:\\'
options_dir['mustexist'] = False
options_dir['title'] = 'Selecciona la carpeta'

directory = tkinter.filedialog.askdirectory(**options_dir)

if len(directory) != 0:
    try:
        iptv_kodi_links = IPTV_KODI_LINKS(directory, option, options_parser.file_option)
        print('Proceso finalizado!')
    except OSError:
        print("Error trying to read file")
