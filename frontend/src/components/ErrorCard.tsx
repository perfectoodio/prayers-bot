import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
interface CardProps {
  message: string | undefined;
}

const ErrorCard: React.FC<CardProps> = ({ message }) => (
  <Card className="bg-red-600 text-white">
    <CardHeader>
      <CardTitle>Error</CardTitle>
    </CardHeader>
    <CardContent>
      <CardDescription className="text-white">{message}</CardDescription>
    </CardContent>
  </Card>
);

export default ErrorCard;
