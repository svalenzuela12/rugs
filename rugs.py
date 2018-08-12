import random
import numpy as np
import threading
import multiprocessing

def TestSquare(square, color):
    for y in range(len(square)):
        for x in range(len(square[y])):
            if square[y][x] != color:
                return False
    return True


def TestRug(num, dimensions, squareSize, colors, outQueue, lock):
    
    #Create random rug
    rug = np.zeros((dimensions[0], dimensions[1]))
    for y in range(dimensions[1]):
        for x in range(dimensions[0]):
            rug[y][x] = random.randint(1, colors)
            
    #Test rug
    for y in range(dimensions[1] - (squareSize[1] - 1)):
        currentColor = -1
        for x in range (dimensions[0]):
            if rug[y][x] == currentColor:
                colorXCount += 1
                if colorXCount >= squareSize[0]:
                    if TestSquare(rug[y + 1 : y + squareSize[1], x - (squareSize[0] - 1) : x + 1], currentColor): # Don't need to test the row we just tested
                        lock.acquire()
                        try:
                            print(f"Rug {num} discarded.\n{rug[y : y + squareSize[1], x - (squareSize[0] - 1) : x + 1]}")
                        finally:
                            lock.release()
                        outQueue.put(True)
                        return
            else:
                currentColor = rug[y][x]
                colorXCount = 1

    #This goes slightly faster if we don't print every rug, but it's boring :)
    lock.acquire()
    try:
        print(f"Rug {num} checked")
    finally:
        lock.release()
    outQueue.put(False)
    return

if __name__ == '__main__':
    
    #Editable Variables
    colors = 3
    dimensions = [100, 100]
    squareSize = [4, 4]
    rugCount = 50000
    maxProcesses = 100

    #Do not edit
    rugsFailed = 0
    pool = multiprocessing.Pool(processes=maxProcesses)
    m = multiprocessing.Manager()
    queue = m.Queue()
    lock = m.Lock()

    #Create worker threads
    for i in range (rugCount):
        pool.apply_async(TestRug, args=(i+1, dimensions, squareSize, colors, queue, lock))

    #Do work
    pool.close()
    pool.join()

    #Get results
    while not queue.empty():
        if queue.get():
            rugsFailed += 1

    #Print results
    print(f"{rugsFailed} rugs discarded.")
    print(f"{(rugsFailed / rugCount) * 100}%")
    wait = input("PRESS ENTER TO CONTINUE.")
       
