import cv2
import numpy as np
import glob
import os

def calibrate_stereo_cameras():
    chessboard_size = (11, 7)  # 12x8 squares => 11x7 inner corners
    square_size = 1.0          # real-world units (e.g., cm)

    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)
    objp *= square_size

    objpoints = []
    imgpoints_left = []
    imgpoints_right = []

    left_images = sorted(glob.glob("calibration_images/data/imgs/leftcamera/*.png"))
    right_images = sorted(glob.glob("calibration_images/data/imgs/rightcamera/*.png"))

    assert len(left_images) == len(right_images), "[❌] Mismatched number of stereo images."

    flags = cv2.CALIB_CB_NORMALIZE_IMAGE + cv2.CALIB_CB_EXHAUSTIVE
    used_pairs = 0

    for left_path, right_path in zip(left_images, right_images):
        img_left = cv2.imread(left_path)
        img_right = cv2.imread(right_path)

        img_left = cv2.resize(img_left, (800, 600))
        img_right = cv2.resize(img_right, (800, 600))

        gray_left = cv2.cvtColor(img_left, cv2.COLOR_BGR2GRAY)
        gray_right = cv2.cvtColor(img_right, cv2.COLOR_BGR2GRAY)
        gray_left = cv2.equalizeHist(gray_left)
        gray_right = cv2.equalizeHist(gray_right)

        ret_left, corners_left = cv2.findChessboardCornersSB(gray_left, chessboard_size, flags)
        ret_right, corners_right = cv2.findChessboardCornersSB(gray_right, chessboard_size, flags)

        if ret_left and ret_right:
            print(f"[✔] Corners found in: {os.path.basename(left_path)} / {os.path.basename(right_path)}")
            objpoints.append(objp)
            imgpoints_left.append(corners_left)
            imgpoints_right.append(corners_right)
            used_pairs += 1

            # Optional preview
            cv2.drawChessboardCorners(img_left, chessboard_size, corners_left, True)
            cv2.drawChessboardCorners(img_right, chessboard_size, corners_right, True)
            cv2.imshow("Stereo Corners", np.hstack((img_left, img_right)))
            cv2.waitKey(100)
        else:
            print(f"[✘] Failed in: {left_path} or {right_path}")

    cv2.destroyAllWindows()
    print(f"[📊] Successfully used {used_pairs} stereo pairs.")

    if used_pairs > 0:
        _, mtx_l, dist_l, _, _ = cv2.calibrateCamera(objpoints, imgpoints_left, gray_left.shape[::-1], None, None)
        _, mtx_r, dist_r, _, _ = cv2.calibrateCamera(objpoints, imgpoints_right, gray_right.shape[::-1], None, None)

        _, _, _, _, _, R, T, E, F = cv2.stereoCalibrate(
            objpoints, imgpoints_left, imgpoints_right,
            mtx_l, dist_l, mtx_r, dist_r,
            gray_left.shape[::-1],
            flags=cv2.CALIB_FIX_INTRINSIC,
            criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5)
        )

        np.savez("stereo_calibration_data.npz",
                 camera_matrix_left=mtx_l,
                 dist_coeffs_left=dist_l,
                 camera_matrix_right=mtx_r,
                 dist_coeffs_right=dist_r,
                 R=R, T=T, E=E, F=F)

        print("[✅] Stereo calibration saved to stereo_calibration_data.npz")
    else:
        print("[❌] Calibration failed. No valid stereo pairs.")

if __name__ == "__main__":
    calibrate_stereo_cameras()