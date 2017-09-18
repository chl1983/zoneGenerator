class zoneGenerator():
    def __init__(self, switch_type, conf_file, command_file, VsanID, cfgname):
        self.__switch_type = switch_type
        self.__conf_file = conf_file
        self.__command_file = command_file
        self.__vsanid = VsanID
        self.__cfgname = cfgname

    def get_var(self, conf_file):
        getwwn = {}
        zone_name_list = []
        error = ''
        with open (conf_file) as mz:
            for line in mz.readlines():
                if 'wwn' in line:
                    x = line.split()
                    port_name = x[1].strip()
                    wwn = x[2].strip()
                    if port_name not in getwwn:
                        getwwn[port_name] = wwn
                    else:
                        error = port_name
                elif 'zn' in line:
                    y = line.split()
                    del y[0]
                    zone_name_list.append(y)
        return(getwwn,zone_name_list,error)

    def brocade_command(self, wwn, zonemember):
        zonelen = len(zonemember)
        zonelen_tmp = 0
        zonename = ''
        wwn_value = ''
        for zonelen_tmp in range(zonelen):
            zonename = zonename+zonemember[zonelen_tmp]+'_'
            wwn_value = wwn_value + wwn[zonemember[zonelen_tmp]]+';'
            zonelen_tmp = zonelen_tmp + 1
        Bcommand = 'zonecreate ' + '"' + zonename[:-1] + '"' + ',' + '"' + wwn_value[:-1]+ '"' + '\n'
        return(Bcommand,zonename)

    def cisco_command(self, wwn, zonemember, vsanid):
        zonelen = len(zonemember)
        zonelen_tmp = 0
        zonename = ''
        wwn_value = ''
        for zonelen_tmp in range(zonelen):
            zonename = zonename+zonemember[zonelen_tmp]+'_'
            wwn_value = wwn_value + 'member pwwn ' + wwn[zonemember[zonelen_tmp]] + '\n'
            zonelen_tmp = zonelen_tmp + 1
        Ccommand = 'zone name '+ zonename[:-1] + ' vsan ' + vsanid + '\n' + wwn_value
        return(Ccommand,zonename)


    def generate_cmd(self):
        var1 = self.get_var(self.__conf_file)
        i = len(var1[1])
        if int(self.__switch_type) == 1:
            config_name = str(self.__cfgname)
            m = 0
            B_zone_name_list = ''
            bfile = open(self.__command_file,'w+')
            if any(var1[2]):
                bfile.write("The WWN alias is not unique!!\n")
                bfile.write(var1[2])
                bfile.close
            else:
                while m < i:
                    wwn = var1[0]
                    zonemember = var1[1][m]
                    bfile.write(str(self.brocade_command(wwn,zonemember)[0]))
                    B_zone_name = str(self.brocade_command(wwn,zonemember)[1])
                    B_zone_name_list = B_zone_name_list + B_zone_name[:-1] + ';'
                    m = m+1
                cfgadd_cmd = 'cfgadd ' + '"' + config_name + '"' + ',' + '"' + B_zone_name_list[:-1] + '"'
                bfile.write(str(cfgadd_cmd))
                bfile.write('\n' + 'Please enable the configuration manually!!!!!')
            bfile.close

        elif int(self.__switch_type) == 2:
            vsanid = self.__vsanid
            zoneset_name = self.__cfgname
            n = 0
            C_zone_name_list = ''
            cfile = open(self.__command_file,'w+')
            if any(var1[2]):
                cfile.write("The WWN alias is not unique!!\n")
                cfile.write(var1[2])
            else:
                while n < i:
                    wwn = var1[0]
                    zonemember = var1[1][n]
                    cfile.write(str(self.cisco_command(wwn, zonemember, vsanid)[0]))
                    C_zone_name = str(self.cisco_command(wwn, zonemember, vsanid)[1])
                    C_zone_name_list = C_zone_name_list + 'member ' + C_zone_name[:-1] + '\n'
                    n = n+1
                zonesetadd_cmd =  'zoneset name '+ zoneset_name + ' vsan ' + vsanid + '\n' + C_zone_name_list
                cfile.write(str(zonesetadd_cmd))
                cfile.write('\n' + 'Please activate the zoneset manually!!!!!')
            cfile.close

#if __name__ == '__main__':
#    conf_file = input("Please input the configuration file: ")
#    command_file = input("Please input the command file: ")
#    switch_type = input("Please select 1:Brocade or 2:Cisco switch: ")
#    VsanID =  input("Please input the vsan id: ")
#    cfgname = input("please input the cfgname or zoneset:")
#    zg = zoneGenerator(switch_type, conf_file, command_file, VsanID, cfgname)
#    zg.generate_cmd()