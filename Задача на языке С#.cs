using System;

namespace Rectangles;

public static class RectanglesTask
{
    // Пересекаются ли два прямоугольника (пересечение только по границе также считается пересечением)
    public static bool AreIntersected(Rectangle r1, Rectangle r2)
    {
        // Если один прямоугольник полностью справа\слева\сверху\снизу ,
        // То прямоугольники не пересекаются

        if (r1.Right < r2.Left) return false;
        if (r2.Right < r1.Left) return false;
        if (r2.Bottom < r1.Top) return false;
        if (r1.Bottom < r2.Top) return false;
        return true;
    }

    // Площадь пересечения прямоугольников
    public static int IntersectionSquare(Rectangle r1, Rectangle r2)
    {
        // Прямоугольники должны пересекаться
        if (!AreIntersected(r1, r2))
            return 0;
        // Находим координаты пересечения
        int left = Math.Max(r1.Left, r2.Left);
        int right = Math.Min(r1.Right, r2.Right);
        int top = Math.Max(r1.Top, r2.Top);
        int bottom = Math.Min(r1.Bottom, r2.Bottom);

        // Вычисляем ширину и высоту пересечения
        int width = right - left;
        int height = bottom - top;

        // Если ширина или высоты <=0, то пересечения нет
        if (width <= 0 || height <= 0)
            return 0;

        // Вычисляем площадь
        int square = width * height;
        return square;
    }

    // Если один из прямоугольников целиком находится внутри другого — вернуть номер (с нуля) внутреннего.
    // Иначе вернуть -1
    // Если прямоугольники совпадают, можно вернуть номер любого из них.
    public static int IndexOfInnerRectangle(Rectangle r1, Rectangle r2)
    {
        // r1 вложен в r2
        if (r1.Left >= r2.Left &&
            r1.Right <= r2.Right &&
            r1.Top >= r2.Top &&
            r1.Bottom <= r2.Bottom)
        {
            return 0;
        }
        // r2 вложен в r1
        if (r2.Left >= r1.Left &&
           r2.Right <= r1.Right &&
           r2.Top >= r1.Top &&
           r2.Bottom <= r1.Bottom)
        {
            return 1;
        }
        // Иначе они не вложены
        return -1;
    }
}
