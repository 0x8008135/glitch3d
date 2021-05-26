import numpy as np


class chip:
    def __init__(self):
        # origin
        self._home_x = 0.0
        self._home_y = 0.0

        # max value for X Y
        self._end_x = 0.0
        self._end_y = 0.0

        # steps
        self.steps = 0.0

    def __len__(self):
        X, Y = self._generate_mesh()
        return len(X) * len(Y)

    def _generate_mesh(self):
        """
        Generate the base mesh. Based on the relative positions and the steps
        """
        if self._home_x > self._end_x:
            x_steps = -self.steps
        else:
            x_steps = self.steps
        x = np.arange(self._home_x, self._end_x + x_steps, x_steps)

        if self._home_y > self._end_y:
            y_steps = -self.steps
        else:
            y_steps = self.steps
        y = np.arange(self._home_y, self._end_y + y_steps, y_steps)

        X, Y = np.meshgrid(x, y)
        for i in range(len(X)):
            if i % 2:
                X[i] = X[i][::-1]
        return X, Y

    def set_home(self, x, y):
        """
        Set home X and Y coordinates
        """
        self._home_x = x
        self._home_y = y

    def set_end(self, x, y):
        """
        Set end (ie. opposite corner) X and Y coordinates
        """
        self._end_x = x
        self._end_y = y

    def random(self):
        """
        Randomly test all positions
        """
        X, Y = self._generate_mesh()
        coordinates = np.vstack([X.ravel(), Y.ravel()]).T
        coordinates = np.random.permutation(coordinates)
        for x, y in coordinates:
            yield (x, y)

    def horizontal(self):
        """
        Scan region horizontally (X) first
        """
        ###############
        # default mode#
        # 0 >->->->-v #
        # 1 v-<-<-<-< #
        # 2 >->->->-> #
        ###############
        X, Y = self._generate_mesh()
        coordinates = np.vstack([X.ravel(), Y.ravel()]).T
        for x, y in coordinates:
            yield (x, y)

    def vertical(self):
        """
        Scan region vertically (Y) first
        """
        ################
        # vertical mode#
        # 0 .>v|.>v|^>.#
        # 1 ^|v|^|v|^|v#
        # 2 ^|.>^|.>^|v#
        ################
        X, Y = self._generate_mesh()
        coordinates = np.vstack([X.ravel(), Y.ravel()]).T
        coordinates = np.vstack(np.flipud([X.ravel(), Y.ravel()])).T
        for x, y in coordinates:
            yield (x, y)
