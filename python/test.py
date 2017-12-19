from LoRaPackage import *
import random

package=LoRaPackage("02","01","123456")
package.setFETCH("LNode","02","10.5","Running")
package.set_command_id(124)
print(package.wrap("str"))


def generatePP(digit:int):
    sample=['1','2','3','4','5','6','7','8','9','0',
            'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
            'A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z'
            ]
    PP=""
    while digit>0:
        PP+=sample[int(random.random()*len(sample))]
        digit-=1
    return PP

print(generatePP(10))

a=[1,2]
try:
    for i in a[4:]:
        print(i)
except:
    print("fuck")