import cv2
import numpy as np
import requests
import time
import threading
import structlog
import logging


def send_message():
    msg = "Motion detected"
    logger.info("send_message", message=msg)

    with lock:
        try:
            requests.post("http://127.0.0.1:5000/message", json={"message": msg})
        except Exception as err:
            logger.error("send_message", error=err)
        global last_alert_time
        last_alert_time = time.time()


def main():
    logger.info("starting_motion_detector")
    # Code for motion detection can be found here
    #   https://sokacoding.medium.com/simple-motion-detection-with-python-and-opencv-for-beginners-cdd4579b2319
    cap = cv2.VideoCapture(0)
    last_mean = 0
    detected_motion = False
    frame_rec_count = 0

    while True:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        result = np.abs(np.mean(gray) - last_mean)
        last_mean = np.mean(gray)

        if result > 0.5:
            time_now = time.time()
            if time_now - last_alert_time > 2 and not lock.locked():
                t = threading.Thread(target=send_message)
                threads.append(t)
                t.start()
            detected_motion = True

        if detected_motion:
            frame_rec_count += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            logger.info("exit_key_detected")
            break

    cap.release()
    cv2.destroyAllWindows()
    logger.info("exiting_motion_detector")


if __name__ == "__main__":
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO)
    )

    logger = structlog.get_logger()

    last_alert_time = time.time()
    lock = threading.Lock()
    threads = []

    main()
    for thread in threads:
        thread.join()
