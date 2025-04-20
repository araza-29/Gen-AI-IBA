# from vision.populate_refunds import process_images_in_folder

# if __name__ == "__main__":
#     folder = input("📁 Enter folder path with receipt images: ")
#     process_images_in_folder(folder)
from vision.populate_refunds import run_pipeline

if __name__ == "__main__":
    print("🚀 Starting refund agent...")
    run_pipeline()
    print("✅ Finished processing.")

