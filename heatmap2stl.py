import json
import copy
import docopt

DOC = '''
Usage:
    heatmap2py <fn_data> <start_x> <end_x> <start_y> <end_y> <substrate_height> <gap_width> <scale_x> <scale_y> <scale_z>
'''

'''
Sample data structure of STL

solid ascii
  facet normal 0 0 10
    outer loop
      vertex   0 20 30
      vertex   -20 20 30
      vertex   -20 0 30
    endloop
  endfacet
endsolid
'''

class Triangle(object):

    def __init__(self, 
            normal=[0, 0, 1], 
            vertices=[
                [0, 0, 0],
                [0, 1, 0],
                [1, 1, 0]
                ]):
        # Face up
        self.normal = copy.deepcopy(normal)
        self.vertices = copy.deepcopy(vertices)

    def scale(self, x, y, z):
        for v in self.vertices:
            v[0] *= x
            v[1] *= y
            v[2] *= z
        return self

    def translate(self, x, y, z):
        #print 'before', self.vertices
        for v in self.vertices:
            v[0] += x
            v[1] += y
            v[2] += z
        #print 'after', self.vertices
        return self

    def __str__(self):
        template = '''
facet normal %s %s %s
  outer loop
    vertex   %s %s %s
    vertex   %s %s %s
    vertex   %s %s %s
  endloop
endfacet
'''
        args = self.normal +\
                self.vertices[0] +\
                self.vertices[1] +\
                self.vertices[2] 
        return template % tuple(args)


class TriangleList(list):
    def __init__(self, *args, **kwargs):
        super(TriangleList, self).__init__(*args, **kwargs)

    def __str__(self):
        return '\n'.join([str(t) for t in self])

    def translate(self, *args, **kwargs):
        for t in self:
            t.translate(*args, **kwargs)
        return self

    def scale(self, *args, **kwargs):
        '''
        This scale may not be what you want.
        Use with caution.
        '''
        for t in self:
            t.scale(*args, **kwargs)
        return self


class Square(TriangleList):
    def __init__(self, 
            normal = [0, 0, 1], 
            vertices = [
                [0, 0, 0],
                [1, 0, 0],
                [1, 1, 0],
                [0, 1, 0]
                ],
            *args, **kwargs):
        super(Square, self).__init__(*args, **kwargs)
        self.normal = normal
        self.vertices = vertices
        self.append(Triangle(normal, copy.deepcopy(vertices[0:3])))
        self.append(Triangle(normal, copy.deepcopy(vertices[2:4] + [vertices[0]])))

    @staticmethod
    def gen_z(direction):
        '''
        direction: 1 or -1
        '''
        return Square(
                normal = [0, 0, direction], 
                vertices = [
                    [0, 0, 0],
                    [1, 0, 0],
                    [1, 1, 0],
                    [0, 1, 0]
                    ]
                )

    @staticmethod
    def gen_y(direction):
        '''
        direction: 1 or -1
        '''
        return Square(
                normal = [0, direction, 0], 
                vertices = [
                    [0, 0, 0],
                    [0, 0, 1],
                    [1, 0, 1],
                    [1, 0, 0]
                    ]
                )

    @staticmethod
    def gen_x(direction):
        '''
        direction: 1 or -1
        '''
        return Square(
                normal = [direction, 0, 0], 
                vertices = [
                    [0, 0, 0],
                    [0, 1, 0],
                    [0, 1, 1],
                    [0, 0, 1]
                    ]
                )


class Block(TriangleList):
    def __init__(self, *args , **kwargs):
        super(Block, self).__init__(*args, **kwargs)
        self.append(Square.gen_x(-1))
        self.append(Square.gen_x(1).translate(1, 0, 0))
        self.append(Square.gen_y(-1))
        self.append(Square.gen_y(1).translate(0, 1, 0))
        self.append(Square.gen_z(-1))
        self.append(Square.gen_z(1).translate(0, 0, 1))


class STL(object):
    def __init__(self, triangle_list):
        self.triangle_list = triangle_list

    def __str__(self):
        tmp = 'solid ascii\n%s\nendsolid' % str(self.triangle_list)
        return tmp


def heatmap2stl(data, 
        start_x, end_x, start_y, end_y, 
        substrate_height,
        gap_width,
        scale_x, scale_y, scale_z,
        ):
    tl = TriangleList()
    for (i, row) in enumerate(data[slice(start_x, end_x)]):
        for (j, cell) in enumerate(row[slice(start_y, end_y)]):
            b = Block()
            b.scale(1, 1, cell)
            b.translate(gap_width + i * (1 + gap_width * 2), 
                    gap_width + j * (1 + gap_width * 2), 0)
            tl.append(b)

    tl.translate(0, 0, substrate_height)
    tl.append(Block().scale(
        (end_x - start_x) * (1 + gap_width * 2), 
        (end_y - start_y) * (1 + gap_width * 2), 
        substrate_height))

    return STL(tl.scale(scale_x, scale_y, scale_z))


if __name__ == '__main__':
    #data = json.load(open('mv-relation.json'))
    #stl = heatmap2stl(data, 
    #        0, 14, 0, 14,
    #        0.1, 
    #        0.1,
    #        5, 5, 20)
    #print stl
    args = docopt.docopt(DOC)
    data = json.load(open(args['<fn_data>']))
    stl = heatmap2stl(data, 
            int(args['<start_x>']), 
            int(args['<end_x>']), 
            int(args['<start_y>']), 
            int(args['<end_y>']), 
            float(args['<substrate_height>']), 
            float(args['<gap_width>']), 
            float(args['<scale_x>']), 
            float(args['<scale_y>']), 
            float(args['<scale_z>']))
    print stl
