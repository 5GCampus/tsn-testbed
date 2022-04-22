#!/bin/bash
# this script creates a simple html table in order to compare all test results
source config.conf
devices=("FibroLAN-FalconRX-NEW")
qoss=("No-QoS" "IEEE-802.1p" "TAS1" "TAS2" "TAS3" "TAS4" "TAS5" "txinject-test" "txinject-TAS1-full")
streams=("robotic-NULL-NULL" "tactileGLOVE-NULL-NULL" "audio-NULL-NULL" "videoBBB-NULL-NULL" "robotic-audio-videoBBB" "tactileGLOVE-audio-videoBBB")
sizes=(64 1518)
loads=(0.0 85.0 100.0 150.0 200.0)
pictures=("ifg_audio" "ifg_ccdf" "ifg_cdf" "ifg_robotic" "ifg_video" "latency_audio" "latency_ccdf" "latency_cdf" "latency_robotic" "latency_video")

mkdir -p "${path}html/"
for device in "${devices[@]}";do
    for stream in "${streams[@]}";do
        for qos in "${qoss[@]}";do
            for picture in "${pictures[@]}"; do
                filename="${path}html/${device}_${stream}_${qos}_${picture}.html"
                echo ${filename}
                echo "<!DOCTYPE html>"> ${filename}
                echo "<html lang='en'>">> ${filename}
                echo "<head><meta charset='utf-8'><title>Overview: ${picture}</title></head>" >> ${filename}
                echo "<body><h1 style='font-family: sans serif;'>Overview: $p</h1><table border='1'>" >> ${filename}
                for size in "${sizes[@]}"; do
                    if [[ ${picture} == "latency_ccdf" && ${stream} != *"NULL"* ]]; then
                        echo "<tr>" >> ${filename}
                        picturenamePNG="${device}_${stream}_No-QoS_${size}_0.0percent-separate/plot/${picture}.png"
                        picturenamePDF="${device}_${stream}_No-QoS_${size}_0.0percent-separate/plot/${picture}.pdf"
                        echo "<td style='font-family: sans serif;'>" >> ${filename}
                        echo "Size: ${size}B<br>Load: 0.0%<br>Separate Streams, No-QoS<br>" >> ${filename}
                        echo "<a href='../$picturenamePDF'>" >> ${filename}
                        echo "<img src='../$picturenamePNG' width='400pt'></a>" >> ${filename}
                        echo "</td>" >> ${filename}
                        echo "</tr>" >> ${filename}
                    fi
                    echo "<tr>" >> ${filename}
                    for load in "${loads[@]}"; do
                        picturenamePNG="${device}_${stream}_${qos}_${size}_${load}percent/plot/${picture}.png"
                        picturenamePDF="${device}_${stream}_${qos}_${size}_${load}percent/plot/${picture}.pdf"
                        echo "<td style='font-family: sans serif;'>" >> ${filename}
                        echo "Size: ${size}B<br>Load: ${load}%<br>QoS: ${qos}<br>" >> ${filename}
                        echo "<a href='../$picturenamePDF'>" >> ${filename}
                        echo "<img src='../$picturenamePNG' width='400pt'></a>" >> ${filename}
                        echo "</td>" >> ${filename}
                    done
                    echo "</tr>" >> ${filename}
                done
                echo "</table></body></html>" >> ${filename}
            done
        done
    done
done
