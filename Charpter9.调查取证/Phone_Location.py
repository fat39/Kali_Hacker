from phone import Phone

p = Phone()

def phone_location(phone):
    return p.find(phone)

if __name__ == '__main__':
    print(phone_location('13911053135'))