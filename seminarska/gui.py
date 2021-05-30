from PyQt5.QtChart import QChartView, QChart, QBarSet, QBarSeries, QBarCategoryAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from db import connect_db


class StatsWindow(QChartView):

    def __init__(self, *args, **kwargs):
        super(StatsWindow, self).__init__(*args, **kwargs)

        self.tribes = []
        self.oids = []
        self.fetch_data()

        # initialise database connection
        self.c = connect_db()

        self.setRenderHint(QPainter.Antialiasing)

        chart = QChart()
        self.setChart(chart)

        chart.setTitle('Population statistics')

        chart.setAnimationOptions(QChart.SeriesAnimations)

        series = self.getSeries()
        chart.addSeries(series)

        axis = QBarCategoryAxis()
        axis.append(map(lambda x: str(x), self.get_oids()))

        chart.createDefaultAxes()

        chart.setAxisX(axis, series)

        chart.legend().setVisible(True)
        chart.legend().setAlignment(Qt.AlignBottom)

    def getSeries(self):
        series = QBarSeries()
        stats = self.get_population_stats()
        for tid in stats:
            s = QBarSet(self.get_tribe_name(tid))
            s.append(stats.get(tid))
            series.append(s)
        return series

    def fetch_data(self):
        cur = self.c.cursor()
        cur.execute("SELECT tid, tribe from pleme ORDER BY tid ASC")
        self.tribes = cur.fetchall()
        cur.execute("select distinct oid from gostota_plemena UNION select distinct oid from gostota_populacije")
        self.oids = cur.fetchall()

    def get_population_stats(self):
        cur = self.c.cursor()
        m = {}
        cur.execute("select * from gostota_plemena "
                    "UNION "
                    "select oid, density, null from gostota_populacije order by oid")
        results = cur.fetchall()
        for res in results:
            oid, density, tid = res
            if not m.get(oid):
                m[oid] = {}
            m[oid][tid] = density
        res = {}
        for tid in self.get_tribe_ids():
            res[tid] = []
            for oid in self.get_oids():
                res[tid].append(m[oid].get(tid) if m[oid].get(tid) else 0)
        return res

    def get_tribe_name(self, tid):
        return self.get_tribe_names()[tid - 1]

    def get_tribe_names(self):
        return list(map(lambda x: str(x[1]), self.tribes))

    def get_tribe_ids(self):
        return list(map(lambda x: x[0], self.tribes))

    def get_oids(self):
        return list(map(lambda x: x[0], self.oids))


def run_app():
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    w = StatsWindow()
    w.setGeometry(0, 0, size.width(), size.height())
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    run_app()
