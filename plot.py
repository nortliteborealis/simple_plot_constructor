import matplotlib.pyplot as plt
import numpy as np


class PlotError(Exception):
    pass


class Plot(object):

    def __init__(self,
                 need_pi_marks=False,
                 need_grid=False,
                 need_legend=False):
        self._start_value = -20
        self._stop_value = 20
        self._step = 0.01
        self._legend = []
        self._need_pi_marks = need_pi_marks
        self._need_grid = need_grid
        self._need_legend = need_legend

    @property
    def need_legend(self):
        return self._need_legend

    @need_legend.setter
    def need_legend(self, value):
        if not isinstance(value, bool):
            raise PlotError('Переменная должна принимать булево значение.')
        self._need_legend = value

    @property
    def legend(self):
        return self._legend

    @legend.setter
    def legend(self, value):
        self._legend.append(str(value))

    @property
    def need_grid(self):
        return self._need_grid

    @need_grid.setter
    def need_grid(self, value):
        if not isinstance(value, bool):
            raise PlotError('Переменная должна принимать булево значение.')
        self._need_grid = value

    @property
    def need_pi_marks(self):
        return self._need_pi_marks

    @need_pi_marks.setter
    def need_pi_marks(self, value):
        if not isinstance(value, bool):
            raise PlotError('Переменная должна принимать булево значение.')
        self._need_pi_marks = value

    @property
    def start_value(self):
        return self._start_value

    @start_value.setter
    def start_value(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise PlotError('Начальное значение графика должно быть числом.')
        if value > self.stop_value:
            raise PlotError('Начальное значение графика должно быть меньше '
                            'конечного значения.')
        self._start_value = value

    @property
    def stop_value(self):
        return self._stop_value

    @stop_value.setter
    def stop_value(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise PlotError('Конечное значение графика должно быть числом.')
        if value < self.start_value:
            raise PlotError('Конечное значение графика должно быть больше '
                            'начального значения.')
        self._stop_value = value

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self, value):
        if not isinstance(value, int) and not isinstance(value, float):
            raise PlotError('Значение шага графика должно быть числом.')
        if value <= 0:
            raise PlotError('Значение шага графика должно быть больше нуля.')
        self._step = value

    def set_plot_ranges(self, start_value, stop_value, step):
        self.start_value = start_value
        self.stop_value = stop_value
        self.step = step

    def get_args(self, func):
        x = np.arange(self.start_value, self.stop_value, self.step)
        y = [func(value) for value in x]
        return x, y

    def add_plot_by_func(self, func, legend='', inverse=False):
        self.legend = legend if legend else func.__name__
        x, y = self.get_args(func)
        if inverse:
            x, y = y, x
        plt.plot(x, y)

    def add_plot_by_args(self, x, y, legend='', inverse=False):
        self.legend = legend if legend else 'func by args'
        if inverse:
            x, y = y, x
        plt.plot(x, y)

    def get_pi_marks(self):
        pi_6_marks = []
        pi_4_marks = []
        pi_6_mark = 0
        pi_4_mark = 0
        first_flag = False
        second_flag = False
        while True:
            if pi_4_mark > self.stop_value:
                first_flag = True
            else:
                pi_4_mark += np.pi / 4
                pi_4_marks.append(pi_4_mark)
                pi_4_marks.append(-pi_4_mark)
            if pi_6_mark > self.stop_value:
                second_flag = True
            else:
                pi_6_mark += np.pi / 6
                pi_6_marks.append(pi_6_mark)
                pi_6_marks.append(-pi_6_mark)
            if first_flag and second_flag:
                break
        return pi_4_marks, pi_6_marks

    def set_pi_marks(self):
        pi_4_marks, pi_6_marks = self.get_pi_marks()
        y = np.zeros(np.shape(pi_4_marks))
        plt.scatter(pi_4_marks, y, marker='|', s=20, c='green')
        y = np.zeros(np.shape(pi_6_marks))
        plt.scatter(pi_6_marks, y, marker='|', s=20, c='red')

    def show_plot(self):
        plt.axvline(alpha=1,
                    linestyle='--',
                    color='black',
                    linewidth=1)
        plt.axhline(alpha=1,
                    linestyle='--',
                    color='black',
                    linewidth=1)
        if self.need_grid:
            plt.grid()
        if self.need_legend:
            plt.legend(self.legend)
        if self.need_pi_marks:
            self.set_pi_marks()
        plt.xlim(-16, 16)
        plt.ylim(-6, 6)
        mngr = plt.get_current_fig_manager()
        mngr.window.showMaximized()
        plt.subplots_adjust(top=0.98,
                            bottom=0.035,
                            left=0.015,
                            right=0.99,
                            hspace=0.2,
                            wspace=0.2)
        plt.show()


if __name__ == '__main__':
    p = Plot()
    p.need_grid = True
    p.need_legend = True
    p.need_pi_marks = True
    p.add_plot_by_func(np.sin)
    p.add_plot_by_func(np.cos)
    p.add_plot_by_func(lambda x: x**2 + x/2)
    p.show_plot()
