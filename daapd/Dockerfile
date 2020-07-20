FROM ubuntu:latest

ENV DEBIAN_FRONTEND noninteractive
ENV LANG en_US.UTF-8
ENV LC_ALL C.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN apt-get -q update &&\
  apt-get install -y wget apt-utils avahi-daemon gnupg

RUN wget -q -O - https://apt.mopidy.com/mopidy.gpg | apt-key add -
RUN wget -q -O /etc/apt/sources.list.d/mopidy.list https://apt.mopidy.com/buster.list
RUN apt-get -q update
RUN apt-get install -y \
  build-essential git autotools-dev autoconf automake libtool gettext gawk gperf \
    antlr3 libantlr3c-dev libconfuse-dev libunistring-dev libsqlite3-dev \
    libavcodec-dev libavformat-dev libavfilter-dev libswscale-dev libavutil-dev \
    libasound2-dev libmxml-dev libgcrypt20-dev libavahi-client-dev zlib1g-dev \
    libevent-dev libplist-dev libsodium-dev libjson-c-dev libwebsockets-dev libcurl4-openssl-dev libspotify12 libspotify-dev

RUN git clone https://github.com/ejurgensen/forked-daapd.git &&\
  cd forked-daapd &&\
  autoreconf -i &&\
  ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --enable-lastfm --enable-mpd --enable-spotify &&\
  make &&\
  make install

VOLUME /log
VOLUME /cache
VOLUME /mnt
EXPOSE 3689

RUN useradd -ms /nologin daapd

COPY forked-daapd.conf /etc/

ADD ./start.sh /start.sh
RUN chmod u+x  /start.sh

CMD ["/start.sh"]
