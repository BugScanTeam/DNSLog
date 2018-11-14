#!/usr/bin/env sh

# dnslog Domain api


########  Public functions #####################

#Usage: add  _acme-challenge.www.domain.com   "XKrxpRBosdIKFzxW_CT3KLZNf6q0HG9i01zxXp5CPBs"
dns_log_add() {
  fulldomain=$1
  txtvalue=$2
  echo "$txtvalue" >> "/tmp/$fulldomain."

}

#fulldomain txtvalue
dns_log_rm() {
  fulldomain=$1
  txtvalue=$2
  sed -i "/$txtvalue/d" "/tmp/$fulldomain."
}