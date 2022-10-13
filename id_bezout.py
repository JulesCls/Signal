
def PGCDRec(a,b):
    if b==0:
        return (a,1,0)
    else:
        d,u,v = PGCDRec(b, a%b)
        return (d,u,v - (a%b)*v)

print(PGCDRec(781,127))
