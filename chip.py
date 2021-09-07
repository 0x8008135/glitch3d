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
        it = 0
        y_start = self._home_y
        while y_start <= self._end_y:
            if it % 2:
                x_start = self._end_x
                while x_start >= self._home_x:
                    yield (x_start, y_start)
                    x_start -= self.steps 
            else:
                x_start = self._home_x
                while x_start <= self._end_x:
                    yield (x_start, y_start)
                    x_start += self.steps 
            y_start += self.steps 
            it += 1

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
        it = 0
        x_start = self._home_x
        while x_start <= self._end_x:
            if it % 2:
                y_start = self._end_y
                while y_start >= self._home_y:
                    yield (x_start, y_start)
                    y_start -= self.steps
            else:
                y_start = self._home_y
                while y_start <= self._end_y:
                    yield (x_start, y_start)
                    y_start += self.steps
            x_start += self.steps
            it += 1

    def spiral_inward(self):
        """
        Scan region in spiral from border to the center
        """
        x_start = self._home_x
        y_start = self._home_y
        direction = 0
        x_steps = int(self._end_x / self.steps)
        y_steps = int(self._end_y / self.steps)
        while x_steps > 0 or y_steps > 0:
            if direction % 4 == 0:
                for x in range(x_steps):
                    yield (x_start, y_start)
                    x_start += self.steps
                if direction != 0:
                    y_steps -= 1
            elif direction % 4 == 1:
                for y in range(y_steps):
                    yield (x_start, y_start)
                    y_start += self.steps
                if direction != 1:
                    x_steps -= 1
            elif direction % 4 == 2:
                for x in range(x_steps):
                    yield (x_start, y_start)
                    x_start -= self.steps
                y_steps -= 1
            elif direction % 4 == 3:
                for y in range(y_steps):
                    yield (x_start, y_start)
                    y_start -= self.steps
                x_steps -= 1
            direction += 1
        yield (x_start, y_start)


    def spiral_outward(self):
        """
        Scan region in spiral from the center to the outside
        """
        x_start = round(self._end_x / 2.0)
        y_start = round(self._end_y / 2.0)
        direction = 0
        nb_steps = 1
        while x_start <= self._end_x and y_start <= self._end_y:
            if direction % 4 == 0:
                for x in range(nb_steps):
                    yield (x_start, y_start)
                    x_start -= self.steps
            elif direction % 4 == 1:
                for y in range(nb_steps):
                    yield (x_start, y_start)
                    y_start -= self.steps
                nb_steps += 1
            elif direction % 4 == 2:
                for x in range(nb_steps):
                    yield (x_start, y_start)
                    x_start += self.steps
            elif direction % 4 == 3:
                for y in range(nb_steps):
                    yield (x_start, y_start)
                    y_start += self.steps
                nb_steps += 1
            direction += 1
