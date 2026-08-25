import speedtest


def check_internet_speed():
    st = speedtest.Speedtest()

    st.get_best_server()

    download_speed = st.download() / 1_000_000
    upload_speed = st.upload() / 1_000_000

    return {
        "download_speed_mbps": round(download_speed, 2),
        "upload_speed_mbps": round(upload_speed, 2),
        "ping_ms": round(st.results.ping, 2)
    }