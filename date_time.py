from datetime import datetime

def date_time():
    """return current date time formatted"""
    now = datetime.now()
    formatted_datetime = now.strftime("%d-%B-%Y %H:%M")
    return formatted_datetime

def main():
    """ test code """
    date_time()

if __name__ == "__main__":
    main()