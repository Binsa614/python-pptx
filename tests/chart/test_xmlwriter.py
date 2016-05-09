# encoding: utf-8

"""
Test suite for pptx.chart.xmlwriter module
"""

from __future__ import absolute_import, print_function, unicode_literals

from itertools import islice

import pytest

from pptx.chart.data import BubbleChartData, ChartData, XyChartData
from pptx.chart.xmlwriter import (
    _BarChartXmlWriter, _BubbleChartXmlWriter, ChartXmlWriter,
    _LineChartXmlWriter, _PieChartXmlWriter, _RadarChartXmlWriter,
    _XyChartXmlWriter
)
from pptx.enum.chart import XL_CHART_TYPE

from ..unitutil import count
from ..unitutil.file import snippet_text
from ..unitutil.mock import class_mock, instance_mock


class DescribeChartXmlWriter(object):

    def it_contructs_an_xml_writer_for_a_chart_type(self, call_fixture):
        chart_type, series_seq_, XmlWriterClass_, xml_writer_ = call_fixture
        xml_writer = ChartXmlWriter(chart_type, series_seq_)
        XmlWriterClass_.assert_called_once_with(chart_type, series_seq_)
        assert xml_writer is xml_writer_

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('BAR_CLUSTERED',                _BarChartXmlWriter),
        ('BAR_STACKED_100',              _BarChartXmlWriter),
        ('BUBBLE',                       _BubbleChartXmlWriter),
        ('BUBBLE_THREE_D_EFFECT',        _BubbleChartXmlWriter),
        ('COLUMN_CLUSTERED',             _BarChartXmlWriter),
        ('LINE',                         _LineChartXmlWriter),
        ('PIE',                          _PieChartXmlWriter),
        ('RADAR',                        _RadarChartXmlWriter),
        ('RADAR_FILLED',                 _RadarChartXmlWriter),
        ('RADAR_MARKERS',                _RadarChartXmlWriter),
        ('XY_SCATTER',                   _XyChartXmlWriter),
        ('XY_SCATTER_LINES',             _XyChartXmlWriter),
        ('XY_SCATTER_LINES_NO_MARKERS',  _XyChartXmlWriter),
        ('XY_SCATTER_SMOOTH',            _XyChartXmlWriter),
        ('XY_SCATTER_SMOOTH_NO_MARKERS', _XyChartXmlWriter),
    ])
    def call_fixture(self, request, series_seq_):
        chart_type_member, XmlWriterClass = request.param
        xml_writer_ = instance_mock(request, XmlWriterClass)
        class_spec = 'pptx.chart.xmlwriter.%s' % XmlWriterClass.__name__
        XmlWriterClass_ = class_mock(
            request, class_spec, return_value=xml_writer_
        )
        chart_type = getattr(XL_CHART_TYPE, chart_type_member)
        return chart_type, series_seq_, XmlWriterClass_, xml_writer_

    # fixture components ---------------------------------------------

    @pytest.fixture
    def series_seq_(self, request):
        return instance_mock(request, tuple)


class Describe_BarChartXmlWriter(object):

    def it_can_generate_xml_for_bar_type_charts(self, xml_fixture):
        xml_writer, expected_xml = xml_fixture
        assert xml_writer.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('BAR_CLUSTERED',    2, 2, '2x2-bar-clustered'),
        ('BAR_STACKED_100',  2, 2, '2x2-bar-stacked-100'),
        ('COLUMN_CLUSTERED', 2, 2, '2x2-column-clustered'),
    ])
    def xml_fixture(self, request):
        enum_member, cat_count, ser_count, snippet_name = request.param
        chart_type = getattr(XL_CHART_TYPE, enum_member)
        series_data_seq = make_series_data_seq(cat_count, ser_count)
        xml_writer = _BarChartXmlWriter(chart_type, series_data_seq)
        expected_xml = snippet_text(snippet_name)
        return xml_writer, expected_xml


class Describe_BubbleChartXmlWriter(object):

    def it_can_generate_xml_for_bubble_charts(self, xml_fixture):
        xml_writer, expected_xml = xml_fixture
        assert xml_writer.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('BUBBLE',                2, 3, '2x3-bubble'),
        ('BUBBLE_THREE_D_EFFECT', 2, 3, '2x3-bubble-3d'),
    ])
    def xml_fixture(self, request):
        enum_member, ser_count, point_count, snippet_name = request.param
        chart_type = getattr(XL_CHART_TYPE, enum_member)
        chart_data = make_bubble_chart_data(ser_count, point_count)
        xml_writer = _BubbleChartXmlWriter(chart_type, chart_data)
        expected_xml = snippet_text(snippet_name)
        return xml_writer, expected_xml


class Describe_LineChartXmlWriter(object):

    def it_can_generate_xml_for_a_line_chart(self, xml_fixture):
        xml_writer, expected_xml = xml_fixture
        assert xml_writer.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def xml_fixture(self, request):
        series_data_seq = make_series_data_seq(cat_count=2, ser_count=2)
        xml_writer = _LineChartXmlWriter(
            XL_CHART_TYPE.LINE, series_data_seq
        )
        expected_xml = snippet_text('2x2-line')
        return xml_writer, expected_xml


class Describe_PieChartXmlWriter(object):

    def it_can_generate_xml_for_a_pie_chart(self, xml_fixture):
        xml_writer, expected_xml = xml_fixture
        assert xml_writer.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture
    def xml_fixture(self, request):
        series_data_seq = make_series_data_seq(cat_count=3, ser_count=1)
        xml_writer = _PieChartXmlWriter(XL_CHART_TYPE.PIE, series_data_seq)
        expected_xml = snippet_text('3x1-pie')
        return xml_writer, expected_xml


class Describe_XyChartXmlWriter(object):

    def it_can_generate_xml_for_xy_charts(self, xml_fixture):
        xml_writer, expected_xml = xml_fixture
        assert xml_writer.xml == expected_xml

    # fixtures -------------------------------------------------------

    @pytest.fixture(params=[
        ('XY_SCATTER',                   2, 3, '2x3-xy'),
        ('XY_SCATTER_LINES',             2, 3, '2x3-xy-lines'),
        ('XY_SCATTER_LINES_NO_MARKERS',  2, 3, '2x3-xy-lines-no-markers'),
        ('XY_SCATTER_SMOOTH',            2, 3, '2x3-xy-smooth'),
        ('XY_SCATTER_SMOOTH_NO_MARKERS', 2, 3, '2x3-xy-smooth-no-markers'),
    ])
    def xml_fixture(self, request):
        enum_member, ser_count, point_count, snippet_name = request.param
        chart_type = getattr(XL_CHART_TYPE, enum_member)
        chart_data = make_xy_chart_data(ser_count, point_count)
        xml_writer = _XyChartXmlWriter(chart_type, chart_data)
        expected_xml = snippet_text(snippet_name)
        return xml_writer, expected_xml


# helpers ------------------------------------------------------------

def make_bubble_chart_data(ser_count, point_count):
    """
    Return an |BubbleChartData| object populated with *ser_count* series,
    each having *point_count* data points.
    """
    points = (
        (1.1, 11.1, 10.0), (2.1, 12.1, 20.0), (3.1, 13.1, 30.0),
        (1.2, 11.2, 40.0), (2.2, 12.2, 50.0), (3.2, 13.2, 60.0),
    )
    chart_data = BubbleChartData()
    for i in range(ser_count):
        series_label = 'Series %d' % (i+1)
        series = chart_data.add_series(series_label)
        for j in range(point_count):
            point_idx = (i * point_count) + j
            x, y, size = points[point_idx]
            series.add_data_point(x, y, size)
    return chart_data


def make_series_data_seq(cat_count, ser_count):
    """
    Return a sequence of |_SeriesData| objects populated with *cat_count*
    category names and *ser_count* sequences of point values. Values are
    auto-generated.
    """
    category_names = ('Foo', 'Bar', 'Baz', 'Boo', 'Far', 'Faz')
    point_values = count(1.1, 1.1)
    chart_data = ChartData()
    chart_data.categories = category_names[:cat_count]
    for idx in range(ser_count):
        series_title = 'Series %d' % (idx+1)
        series_values = tuple(islice(point_values, cat_count))
        series_values = [round(x*10)/10.0 for x in series_values]
        chart_data.add_series(series_title, series_values)
    return chart_data.series


def make_xy_chart_data(ser_count, point_count):
    """
    Return an |XyChartData| object populated with *ser_count* series each
    having *point_count* data points. Values are auto-generated.
    """
    points = (
        (1.1, 11.1), (2.1, 12.1), (3.1, 13.1),
        (1.2, 11.2), (2.2, 12.2), (3.2, 13.2),
    )
    chart_data = XyChartData()
    for i in range(ser_count):
        series_label = 'Series %d' % (i+1)
        series = chart_data.add_series(series_label)
        for j in range(point_count):
            point_idx = (i * point_count) + j
            x, y = points[point_idx]
            series.add_data_point(x, y)
    return chart_data
