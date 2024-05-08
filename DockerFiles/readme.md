## Docker m1 run
`docker run -e DISPLAY=$(ifconfig en0 | grep inet | awk '$1=="inet" {print $2}'):0 \
           -v /tmp/.X11-unix:/tmp/.X11-unix \
           -v "/Users/$(whoami)/VoxNovel:/VoxNovel" \
           athomasson2/voxnovel:m1_latest
`

## Docker headless m1 run
`docker run -it -v "/Users/$(whoami)/VoxNovel:/VoxNovel" athomasson2/voxnovel:headless_m1_latest`
