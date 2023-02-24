from compModule import compMod
from trackModule import trackMod
import time

if __name__ == "__main__":
    comps = compMod()
    track = trackMod()
    comps.start()
    track.start()

    while True:
        time.sleep(0.25)
        print(comps.competitors)
        print(track.RaceTrack)
