import csv
import random
import math
import copy
import operator
import decimal

def loadDataset(filename):
    with open(filename,'rb') as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)
        panjang = len(dataset[0])
        jumlah = len(dataset)
        missVal(dataset,panjang)
        for x in range(len(dataset)-1):
            for y in range(panjang -1):
                dataset[x][y] = float(dataset[x][y])
        return dataset,panjang,jumlah

def findRata(dataset,index): #mencari rata"
    jumlah=0 #buat nyari jumlah yang gak missing value
    total=0 #buat jumlah nilai
    for x in range(len(dataset)-1):
        if dataset[x][index] !=0:
            jumlah+=1
            #print str(x)+" "+str(index)
            total+=float(dataset[x][index])
    return float(float(total)/float(jumlah))

def missVal(dataset,panjang): #mencari missing value
    for x in range(panjang-1):
        rata = findRata(dataset,x)
        for y in range(len(dataset)-1):
            if dataset[y][x] == 0:
                dataset[y][x] = rata

def eucledianDistance (instance1,instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x]-instance2[x]),2)
    return math.sqrt(distance)



def pickRandom(dataset,cluster,index=[]): #buat ambil random titik awal
    print "Centroid awal:"
    for i in range(cluster):
        pick=random.randint(0,len(dataset)-1)
        take=True
        stop=False
        while(not stop):
            take=True
            stop=False
            if(len(index)==0):
                stop=True
            for x in range(len(index)):
                if index[x]==pick:
                    take=False
                    stop=False
            if(take):
                stop=True
        if(take):
            index.append(dataset[pick])
            print "Data ke-"+str(pick+1)+": "+str(dataset[pick])


def pickPilih(dataset,cluster,index=[]):
    pick=[]
    for i in range(cluster):
        take = True
        stop = False
        while(not stop):
            stop=False
            take=True
            picking = input("Masukkan data ke-"+str(i+1)+":")
            picking-=1
            if (len(pick)==0):
                stop=True
            for x in range(len(pick)):
                if pick[x]==picking:
                    print "angka sudah dipilih"
                    stop=False
                    take=False
            if picking < 0 or picking > (len(dataset)-2):
                print "angka diluar jumlah data"
                stop=False
                take=False
            if(take):
                stop=True
        pick.append(picking)
    print "Centroid awal:"
    for i in range(cluster):
        index.append(dataset[pick[i]])
        print "Data ke-" + str(pick[i] + 1) + ": " + str(dataset[pick[i]])

def checkNew(centroid,oldCentroid):
    if centroid == oldCentroid:
        return False
    else:
        return True

def findKelas (dataset,kelas=[]):
    for x in range(len(dataset)-1):
        cek = 0
        for i in range(len(kelas)):
            if dataset[x][-1] == kelas[i]:
                cek = 1
        if cek != 1:
            kelas.append(dataset[x][-1])

def kMeans(dataset,centroid,k):
    cluster=[]
    for y in range(k):
        cluster.append([])
    for x in range(len(dataset)-1):
        cek=[]
        terkecil=0
        for y in range(k):
            #print str(x) +" "+str(y)+" "+str(k)+" "+str(len(dataset)-1)
            cek.append(eucledianDistance(dataset[x],centroid[y],len(dataset[0])-1))
            terkecil = min(cek)
        for y in range(k):
            if cek[y] == terkecil:
                cluster[y].append(dataset[x])
    return cluster

def getNewCentroid(cluster,centroid,panjang):
    for x in range(len(cluster)):
        for y in range(panjang-1):
            jumlah = 0.0
            for z in range(len(cluster[x])):
                jumlah += cluster[x][z][y]
            jumlah /= len(cluster[x])
            #print str(x) + " " + str(z) + " " + str(y) + " " + str(len(cluster)) + " " + str(len(cluster[x]) - 1) + " " + str(panjang - 1)
            output=round(jumlah,2)
            #print str(x)+" "+str(y)+" "+str(len(cluster[x][y]))+" "+str(len(centroid))+" "+str(len(centroid[x]))
            centroid[x][y]=output
#def printHasil(cluster,centroid,kelas):

def printBagian(cluster,kelas,x):
    jumlah = 0
    for i in range(len(cluster)):
        if cluster[i][-1]==kelas:
            jumlah+=1
    output = round(float(float(jumlah)/float(len(cluster))),2)
    print "Kelas " + str(kelas) + ":"+str(jumlah)+"/"+str(len(cluster))+" ("+str(output*100)+"%)"


def printHasil(cluster,centroid,kelas,jumlah):
    print "Kelas:"
    for i in range(len(kelas)):
        print kelas[i]
    for i in range(len(centroid)):
        print "\n"
        print "Cluster "+str(i+1)+" (jumlah data: "+str(len(cluster[i]))+"/"+str(jumlah-1)+"):"
        output="Centroid="
        for x in range(len(centroid[i])-1):
            output+=" "+str(centroid[i][x])
            if x != len(centroid):
                output+=";"
        print output
        for x in range(len(kelas)):
            printBagian(cluster[i],kelas[x],x)

def main():
    decimal.getcontext().prec = 2
    dataset=[]
    index=[]
    centroid=[]
    finish=True
    kelas=[]
    cluster=[]
    panjang=0
    jumlah=0
    oldCentroid=[]
    namaFile=raw_input("Masukkan nama file:")
    k = input("Masukkan nilai k:")
    pick = raw_input("Input 0 untuk memilih data centroid, selain 0 untuk data centroid random :")
    dataset,panjang,jumlah=loadDataset(namaFile)
    print "Jumlah data: "+str(jumlah-1)
    print
    if (pick=="0"):
        pickPilih(dataset,k,centroid)
    else:
        pickRandom(dataset,k,centroid) #buat ambil random titik awal
    findKelas(dataset,kelas) #hasilnya array isinya kelas-kelas yang ada (variable kelas isinya berubah)
    while(finish):
        oldCentroid=copy.deepcopy(centroid)
        cluster=kMeans(dataset,centroid,k) #membagi menjadi cluster (variable cluster isiya berubah, isinya pembagian berdasarkan cluster)
        getNewCentroid(cluster,centroid,panjang) #mencari centroid baru (variable centroid isinya berubah, dapet centroid yang baru)
        finish=checkNew(centroid,oldCentroid) #ngecek udah sampe akhir atau belum (variable finish bisa berubah)

    printHasil(cluster,centroid,kelas,jumlah) #print sesuai format
    #generate predictions
#remove
#append

main()