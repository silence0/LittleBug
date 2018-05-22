import traceback
try:
    while True:
        try:
            print(1/0)
            print('nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn')
        except:
            traceback.print_exc()
            pass
except Exception as e:
    print(e)