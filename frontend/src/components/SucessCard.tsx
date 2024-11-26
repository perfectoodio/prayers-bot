import { 
  Card, 
  CardContent, 
  CardHeader, 
  CardTitle, 
  CardDescription 
} from '@/components/ui/card';
interface CardProps {
    message: string | undefined;
  }
const SuccessCard: React.FC<CardProps> = ({ message }) => (
  <Card className="bg-green-600 text-white">
    <CardHeader>
      <CardTitle>Prayer Sent Successfully</CardTitle>
    </CardHeader>
    <CardContent>
      <CardDescription className="text-white">
        {message}
      </CardDescription>
    </CardContent>
  </Card>
);

export default SuccessCard;