import services
import build_buy
from ts4mp.debug.log import ts4mp_log

debug = False

try:
    if debug:
        x, y, z = services.get_active_sim().position
        contours = build_buy.get_wall_contours(x, z, services.get_active_sim().routing_surface, True)
        ts4mp_log("buildbuy", str(contours))

except Exception as e:
    pass