import logging
import seqlog
import time

seqlog.log_to_seq(
   server_url="http://127.0.0.1:5341/",
   api_key="RK2UCFPEIY7dsttQJA9F",
   level=logging.NOTSET,
   batch_size=10,
   auto_flush_timeout=1,  # seconds
   override_root_logger=True,
   # json_encoder_class=json.encoder.JSONEncoder  # Optional; only specify this if you want to use a custom JSON encoder
)

logging.debug("A log message in level debug")
logging.info("A log message in level info")
logging.warning("A log message in level warning")
logging.error("A log message in level error")
logging.critical("A log message in level critical")
logging.info("Hello, {name}!", name="World")

logging.info("Processed order {orderId} by {customer}", 
                     orderId = 15, customer = "Johnny")

try:
    result = 2 / 0
except Exception as exception:
    logging.exception("We got an exception")
    

time.sleep(2) # sleep for 2 seconds to give seqlog time to write to Seq