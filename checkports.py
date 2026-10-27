import socket

runcounter = 0
def main():
    # Since the restart function reruns the main function in the same instance of the program, this makes sure that the function is not called too many times.
    # I am now learning that this was pointless. Well, you learn something every day.
    global runcounter
    if runcounter > 5:
        print('Too many instances running simultaneously. Restart the program')
        raise SystemExit
    def range_func():
        lowb = input2('\nWhat should the range start from? ')
        uppb = input2('\nWhat should the range end at? ')
        if lowb.isdigit() and uppb.isdigit():
            if (int(lowb) >= 0 and int(lowb) <= 65364) and (int(uppb) >= 1 and int(uppb) <= 65365) and (int(uppb) > int(lowb)):
                return list(range(int(lowb),int(uppb)))
            else:
                print('\nInvalid Range!')
                return None
        else:
                print('\nInvalid Range!')
                return None

    # Input for the ports to check. Returns them as a list for the next function
    def ports():
        ports_checked = input2('\033\n[1mWhich ports should we check are open? \033[0m Give each ports as a single number, e.g. "254" followed by a space " ", write "All" to check all ports, or type "Range" to enter a range of ports. Type "exit" at any point to leave the program, or "restart" to start from the beginning. \n \n')
        ports_inputted = ports_checked.split(" ")
        return ports_inputted

    # Returns the ports to a variable after validating the input from the previous function
    def validate_ports(ports_entered):

        ports_to_check = []
        try:
        # Check if the port is an integer within range. If it is we add it to the list og ports to check.
            for item in ports_entered:
                if int(item) >= 0 and int(item) <= 65535:
                    ports_to_check.append(int(item))
                elif not item.isdigit():
                    print(f'\nThis is not a number!')
                    return none
                else:
                    print(f'\nThe number {int(item)} is invalid!')
                    return None
            return ports_to_check
        except ValueError:
        # If one of the items is a letter (hopefully the word 'all') then we handle this elsewhere
                if item.lower().strip() == 'all':
                    return ['all']
                elif item.lower().strip() == 'range':
                    returner = range_func()
                    while returner == None:
                        returner = range_func()
                    return returner
                else:
                    return None
    # The first argument for the function which checks if the ports are open
    ports_to_check_outer = validate_ports(ports())

    while ports_to_check_outer == None:
        ports_to_check_outer = validate_ports(ports())
    # Input for the hostname. Does it by asking for each octet.
    def octets():
        print('\n\033[1mInput each octet of the host name. \033[0m(e.g. 127 in 127.0.0.1)')
        octet1, octet2, octet3, octet4 = input2 ('\nFirst Octet: '), input2 ('\nSecond Octet: '), input2 ('\nThird Octet: '), input2 ('\nFourth Octet: ')
        return octet1.strip(), octet2.strip(), octet3.strip(), octet4.strip()
    # Returns the hostname after input validation
    def check_host(one,two,three,four):
        if (one.isdigit()) and (two.isdigit()) and (three.isdigit()) and (four.isdigit()):
            nums = [int(one), int(two), int(three), int(four)]
            for num in nums:
                if num < 0 or num > 255:
                    print('\nInvalid input! Try again!')
                    return 'None'
        else:
            print('\nInvalid input! Try again!')
            return 'None'
        host_in = f'{one}.{two}.{three}.{four}'
        return host_in


    host = check_host(*octets())
    # Keep asking until they enter a valid hostname
    while host == 'None':
        host = check_host(*octets())

    filename = input2('\n\033[1mAnd finally, what filename do you want your results to be saved to?\033[0m The file be in your current working directory. \n \n')

    def check_ports(ports_check, host_name):
        # I solve everything with counters apparently...
        print_counter = 0
        def print3(text):
            nonlocal print_counter
            print_counter += 1
            if print_counter < 7:
                print(text)
                return
            elif print_counter == 7:
                print('\nRemaining output will go to the text file.')

        ports_closed = []
        ports_open = []
        ports_timed_out = []
    # If specific ports are selected only check these ports:
        for port in ports_check:
            if type(port) == int and (port >= 0 and port <= 65535):
                try:
                    connection = socket.create_connection((host_name, port), timeout = 2)
                    connection.close()
                    ports_open.append(port)
                    print3(f'\nConnection to port {port} successful')
                except TimeoutError:
                    print3(f'\nConnection to port {port} timed out.')
                    ports_timed_out.append(port)
                except:
                    print3(f'\nConnection to port {port} failed. Port may be closed.')
                    ports_closed.append(port)
    # If all is selected check all ports
            elif type(port) == str and (port.lower() == 'all'):
                print('\n\033[1mThis may take a while! \033[0mResults will be printed to the file you specified above.')
                for number in range(0,65535):
                    try:
                        connection = socket.create_connection((host_name, number), timeout = 2)
                        connection.close()
                        ports_open.append(number)
                    except TimeoutError:
                        ports_timed_out.append(number)
                    except:
                        ports_closed.append(number)

        with open(f'{filename}.txt', 'w', encoding = 'utf-8') as result_file:
            result_file.write(f'These ports are open: {str(ports_open)} \n')
            result_file.write(f'These ports timed out: {str(ports_timed_out)} \n')
            result_file.write(f'These ports are likely closed: {str(ports_closed)} \n')

    check_ports(ports_to_check_outer, host)
# I decided I want the user to be able to exit or restart at any point. This was the best way I could think of -  to replace every instance of the input function with this one, which does what the input fucntion does but also checks if the user entered 'exit' or 'restart'.
def input2(value):
    output = input(value)

    if output.lower().strip() == 'exit':
        raise SystemExit
    elif output.lower().strip() == 'restart':
        global runcounter
        runcounter += 1
        main()

    return output
# Call the main function.
main()

