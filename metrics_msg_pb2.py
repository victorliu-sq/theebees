# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: metrics_msg.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11metrics_msg.proto\x12\x07Metrics\"u\n\x07\x43PUDist\x12\x36\n\x0brange2usecs\x18\x01 \x03(\x0b\x32!.Metrics.CPUDist.Range2usecsEntry\x1a\x32\n\x10Range2usecsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x02:\x02\x38\x01\"!\n\x0eMetricsRequest\x12\x0f\n\x07metrics\x18\x01 \x01(\t\"v\n\x0fMetricsResponse\x12!\n\x07\x63pu_avg\x18\x01 \x01(\x0b\x32\x10.Metrics.CPUDist\x12!\n\x07\x63pu_sum\x18\x02 \x01(\x0b\x32\x10.Metrics.CPUDist\x12\x1d\n\x03\x63pu\x18\x03 \x03(\x0b\x32\x10.Metrics.CPUDist2S\n\x0cQueryManager\x12\x43\n\x0cQueryMetrics\x12\x17.Metrics.MetricsRequest\x1a\x18.Metrics.MetricsResponse\"\x00\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'metrics_msg_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CPUDIST_RANGE2USECSENTRY._options = None
  _CPUDIST_RANGE2USECSENTRY._serialized_options = b'8\001'
  _CPUDIST._serialized_start=30
  _CPUDIST._serialized_end=147
  _CPUDIST_RANGE2USECSENTRY._serialized_start=97
  _CPUDIST_RANGE2USECSENTRY._serialized_end=147
  _METRICSREQUEST._serialized_start=149
  _METRICSREQUEST._serialized_end=182
  _METRICSRESPONSE._serialized_start=184
  _METRICSRESPONSE._serialized_end=302
  _QUERYMANAGER._serialized_start=304
  _QUERYMANAGER._serialized_end=387
# @@protoc_insertion_point(module_scope)
