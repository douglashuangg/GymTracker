"""
Created May 14, 2022
Security class from GymTracker project

implement:
dot not allow further typing when entering password reaches max length
only allow user to enter numbers, entering letters is unresponsive

"""

class Security:
    def __init__(self, pass_length = 4, password = 0000):
        self.pass_length = pass_length # ensures that min password length is 4 (standard for pin)
        self.password = password # default password

    def get_length(self):
        pin_length = input('Please enter the length of your PIN (4-8 digits): ')

        try:
            pin_length = int(pin_length)
            if (pin_length >= 4 and pin_length <= 8):
                self.pass_length = pin_length
                return
        except ValueError:
            while (True):
                pin_length = input('Please enter a valid length of your PIN (4-8 digits): ')
                try:
                    pin_length = int(pin_length)
                    if (pin_length >= 4 and pin_length <= 8):
                        self.pass_length = pin_length
                        return
                except ValueError:
                    continue

        self.pass_length = pin_length
        return
            

def main():
    pin = Security()

    print ('PIN Setup Started. Please follow the instructions below.')

    pin.get_length()
    
    print ('end')
    

if __name__ == '__main__':
    main()